import cv2
import numpy as np
import math
 
#Parameter
minArea = 30
maxArea = 50
minThreshold = 50
maxThreshold = 200
stampede_thr = 0.1#0.001
density_of_people = 0.02#3
 
def blob_detector(img):
	img = cv2.bitwise_not(img)
	params = cv2.SimpleBlobDetector_Params()
	params.minThreshold = minThreshold
	params.maxThreshold = maxThreshold
 
	# Filter by Area.
	params.filterByArea = True
	params.minArea = minArea
	params.maxArea = maxArea
 
	# Filter by Circularity
	params.filterByCircularity = False
	params.minCircularity = 0.1
 
	# Filter by Convexity
	params.filterByConvexity = False
	params.minConvexity = 0.87
 
	# Filter by Inertia
	params.filterByInertia = False
	params.minInertiaRatio = 0.01
 
	# Create a detector with the parameters
	ver = (cv2.__version__).split('.')
	if int(ver[0]) < 3 :
		detector = cv2.SimpleBlobDetector(params)
	else :
		detector = cv2.SimpleBlobDetector_create(params)
 
	# Detect blobs.
	keypoints = detector.detect(img)
	blank_image = np.zeros((img.shape[0],img.shape[1],1), np.uint8)
	blank_image[:,:] = 255
 
	h,w,c = blank_image.shape
   
	#Remove points on boundary
	boundary_leave = 0
	try:
		for k in keypoints:
			if (int(k.pt[0]) <= w-boundary_leave and int(k.pt[1]) <= h-boundary_leave and int(k.pt[0]) >= boundary_leave and int(k.pt[1]) >= boundary_leave):
				cv2.circle(blank_image, (int(k.pt[0]), int(k.pt[1])), int(k.size/2), (0, 0, 0), -1)
	except Exception as e:
		print e
	# cv2.imshow('orgImage',img)
	# cv2.imshow('peopleDected',blank_image)
	# cv2.waitKey(0)
	try:
		p2 = []
		p_float = np.empty((0))
		if keypoints :
			for k in keypoints:
				if (int(k.pt[0]) <= w-boundary_leave and int(k.pt[1]) <= h-boundary_leave and int(k.pt[0]) >= boundary_leave and int(k.pt[1]) >= boundary_leave):
					p2.append([[k.pt[0],k.pt[1]]])
			p2 = np.array(p2)
			p_float = p2.astype(np.float32)
	except Exception as e:
		print e
	return (p_float,blank_image)
 
def stampede_detect():   
	video_path = "2.mp4"
	video_path_save_optical = 'optical_flow.avi'
	video_path_save_bg = 'bg.avi'
   
	# fgbg = cv2.createBackgroundSubtractorMOG2()   
	fgbg = cv2.BackgroundSubtractorMOG()


	
	feature_params = dict( maxCorners = 100,qualityLevel = 0.3,minDistance = 7,blockSize = 7 )   
 
	lk_params = dict( winSize  = (15,15),maxLevel = 2,criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
	# Create some random colors
	try:
		cap = cv2.VideoCapture(video_path)
		ret, old_frame = cap.read()
		old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
		p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
	except Exception as e:
		print e
   
	try:
		# fourcc = cv2.VideoWriter_fourcc(*'XVID')
		fourcc = cv2.cv.CV_FOURCC(*'XVID')

		video_optical = cv2.VideoWriter(video_path_save_optical,fourcc,20,(1280,720),0)
 
		video_bg = cv2.VideoWriter(video_path_save_bg,fourcc,20,(1280,720),0)
 
	except Exception as e:
		print e
 
	thr = stampede_thr
 
	count_frame=0
	count_sub_image = 0
	old_gray_sub = []
   
	distance_flow_prev = []
	distance_flow_curr = []
   
	for i in range(0,old_gray.shape[0],old_gray.shape[0]/2):
		for j in range(0,old_gray.shape[1],old_gray.shape[1]/2):
			old_gray_sub.append(old_gray[i:i+old_gray.shape[0]/2,j:j+old_gray.shape[1]/2])
			distance_flow_prev.append(0)
			distance_flow_curr.append(0)           
			count_sub_image = count_sub_image+1
 
	while(count_frame<20):
	# while(1):
		try:
			mask = np.zeros_like(old_gray_sub[0])
			img = np.zeros_like(old_gray)
			ret, frame = cap.read()
			if ret:
				print 'Processing Frame #%d'%count_frame
				frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
				fgmask = fgbg.apply(frame)
 
				# calculate optical flow
				ret_thr ,fgmask_thr = cv2.threshold(fgmask,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)               
				p0,blank_image = blob_detector(fgmask_thr)
				try:
					video_bg.write(blank_image)
				except Exception as e:
					print e
					video_bg.release()
					video_optical.release()					
					break
 
				count_sub_image = 0
				dis = 0
				for i in range(0,frame_gray.shape[0],frame_gray.shape[0]/2):
					for j in range(0,frame_gray.shape[1],frame_gray.shape[1]/2):
						frame_gray_sub = frame_gray[i:i+frame_gray.shape[0]/2,j:j+frame_gray.shape[1]/2]
						fgmask_thr_sub = fgmask_thr[i:i+fgmask_thr.shape[0]/2,j:j+fgmask_thr.shape[1]/2]
						p0,blank_image_sub = blob_detector(fgmask_thr_sub)
						if p0.size:
							# cv2.imshow('frame_gray_sub',frame_gray_sub)
							# cv2.imshow('blank_image_sub',blank_image_sub)
							try:
								p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray_sub[count_sub_image], frame_gray_sub, p0, None, **lk_params)
							except Exception as e:
								print e
							# Select good points
							good_new = p1[st==1]
							good_old = p0[st==1]
 
							# Now update the previous frame and previous points
							old_gray_sub[count_sub_image] = frame_gray_sub.copy()

							# draw the tracks
							mask = np.zeros_like(old_gray_sub[0])
							h_mask,w_mask = mask.shape
							count_points = 0
							for k,(new,old) in enumerate(zip(good_new,good_old)):
								a,b = new.ravel()
								c,d = old.ravel()
								if (a<= w_mask and b<=h_mask and c<= w_mask and d<=h_mask  ):
									#distance moved is
									dis = dis+math.sqrt((a-c)*(a-c)+(b-d)*(b-d))
									# mask = cv2.line(mask, (a,b),(c,d), 255, 4)
									# frame_gray_sub = cv2.circle(frame_gray_sub,(a,b),2,255,4)
									cv2.line(mask, (a,b),(c,d), 255, 4)
									cv2.circle(frame_gray_sub,(a,b),2,255,4)
									count_points = count_points+1
 
							img_sub = cv2.add(frame_gray_sub,mask)
						   
							# cv2.imshow('img_sub',img_sub)                           
							# cv2.waitKey(0)
						   
							distance_flow_curr[count_sub_image] = dis/count_points
							img[i:i+fgmask_thr.shape[0]/2,j:j+fgmask_thr.shape[1]/2]=img_sub.copy()
							p0 = good_new.reshape(-1,1,2)
							number_of_points = frame_gray_sub.shape[0]*frame_gray_sub.shape[1]
							per_of_people = float(count_points/(float)(number_of_points))*100
							print 'Density of crowd %f'%per_of_people
							print 'Diff betweeen optical flow is %f'%(abs(distance_flow_curr[count_sub_image]-distance_flow_prev[count_sub_image]))
 
							if ( per_of_people>density_of_people and abs(distance_flow_curr[count_sub_image]-distance_flow_prev[count_sub_image])<thr and distance_flow_prev[count_sub_image]>0 and distance_flow_curr[count_sub_image]>0):
								cv2.imshow('stampede',img_sub)
								cv2.waitKey(0)
								cv2.rectangle(img_sub,(0,0),(img_sub.shape[1],img_sub.shape[0]),(0,0,0),20)
								img[i:i+fgmask_thr.shape[0]/2,j:j+fgmask_thr.shape[1]/2]=img_sub.copy()								
								print 'Average optical flow curr/prev is %f and %f'%(distance_flow_curr[count_sub_image],distance_flow_prev[count_sub_image])
								print 'Diff betweeen optical flow is %f'%(abs(distance_flow_curr[count_sub_image]-distance_flow_prev[count_sub_image]))
								print 'Stampede Happened'
						else:
							img[i:i+fgmask_thr.shape[0]/2,j:j+fgmask_thr.shape[1]/2]=frame_gray_sub.copy()
						count_sub_image = count_sub_image+1
				count_frame = count_frame+1
				print '\n'
				distance_flow_prev = distance_flow_curr[:]
				try:
					# cv2.imshow('img',img)
					# cv2.waitKey(0)
					video_optical.write(img)
				except Exception as e:
					print e
					video_bg.release()
					video_optical.release()
					break
			else:
				video_bg.release()
				video_optical.release()				
				break
		except Exception as e:
			print e
			video_bg.release()
			video_optical.release()
			break
	video_bg.release()
	video_optical.release()
	cap.release()
	cv2.destroyAllWindows()   
 
stampede_detect()