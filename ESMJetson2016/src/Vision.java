import java.util.ArrayList;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.MatOfInt;
import org.opencv.core.MatOfPoint;
import org.opencv.highgui.VideoCapture;
import org.opencv.imgproc.Imgproc;

import edu.wpi.first.wpilibj.networktables.NetworkTable;

/**
 *
 */
public class Vision {
	
	public static VideoCapture videoCapture;
	public static NetworkTable visionTable;
	
	public static void main(String[] args) {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
		videoCapture = new VideoCapture();  
		videoCapture.open(0);
//		while(!videoCapture.isOpened())
//		{
//			System.out.println("Video not open");
//		}
		setupVisionTable();
		runVision();
		releaseCapture();
	}
	
	public static void setupVisionTable() {
		NetworkTable.setIPAddress("10.46.69.2");
    	NetworkTable.setClientMode();
    	NetworkTable.initialize();
    	visionTable = NetworkTable.getTable("vision");
		
	}

	public static void runVision() {
		while(true) {
			if (visionTable.isConnected() && getRunVision()) {
				Mat frame1 = getCameraImage();
				turnOnLight();
				Mat frame2 = getCameraImage();
				turnOffLight();
				Mat processedFrame = threshold(getGrayscale(getDifference(frame1,frame2)));
				MatOfInt hull = getConvexHull(getMaxContour(getContours(processedFrame)));
				putValuesOnVisionTable(hull);
				setRunVision(false);
			}
		}
		
	}

	private static void putValuesOnVisionTable(MatOfInt hull) {
		
	}

	public static void setRunVision(boolean b) {
		visionTable.putBoolean("runVision", b);
	}

	public static boolean getRunVision() {
		return visionTable.getBoolean("runVision", false);
	}

	public static void releaseCapture() {
		videoCapture.release();
	}
	
	public static void turnOnLight() {
		if (visionTable.getBoolean("lightOn", true) == false) {
			visionTable.putBoolean("lightOn", true);
			while(getLightOnDone() == false) {	
			}
		}
	}
	
	public static boolean getLightOnDone() {
		return visionTable.getBoolean("lightOnDone", false);
	}

	public static void turnOffLight() {
		if (visionTable.getBoolean("lightOn", false) == true) {
			visionTable.putBoolean("lightOn", false);
			while(getLightOnDone()) {	
			}
		}
	}
	
	public static Mat getCameraImage() {
		Mat frame = new Mat();
		videoCapture.retrieve(frame);
		return frame;
	}
	
	public static Mat getDifference(Mat frame1, Mat frame2) {
		Mat diff = new Mat();
		Core.subtract(frame2, frame1, diff);
		return diff;
	}
	
	public static Mat getGrayscale(Mat frame) {
		Mat grayscale = new Mat();
		Imgproc.cvtColor(frame, grayscale, Imgproc.COLOR_RGB2GRAY);
		return grayscale;
	}
	
	public static Mat threshold(Mat frame) {
		Mat newFrame = new Mat();
		Imgproc.threshold(frame, newFrame, 50, 255, Imgproc.THRESH_BINARY);
		return newFrame;
	}
	
	public static ArrayList<MatOfPoint> getContours(Mat frame) {
		ArrayList<MatOfPoint> contoursList = new ArrayList<MatOfPoint>();
		Mat hierarchy = new Mat();
		Imgproc.findContours(frame, contoursList, hierarchy, Imgproc.RETR_LIST, Imgproc.CHAIN_APPROX_SIMPLE);
//		Scalar color = new Scalar( 255, 0, 0 );
//		Imgproc.drawContours(frame, contoursList, -1, color, 3);
		return contoursList;
	}
	
	public static MatOfPoint getMaxContour(ArrayList<MatOfPoint> contoursList) {
		MatOfPoint maxContour = new MatOfPoint();
		if (contoursList.size()>0) {
			maxContour = contoursList.get(0);
			double maxArea = Imgproc.contourArea(maxContour);
			for (MatOfPoint contour:contoursList) {
				double area = Imgproc.contourArea(contour);
				if (area>maxArea) {
					maxContour = contour;
					maxArea = area;
				}
			}
		}
		return maxContour;
	}
	
	public static MatOfInt getConvexHull(MatOfPoint contour) {
		MatOfInt hull = new MatOfInt();
		Imgproc.convexHull(contour, hull);
		return hull;
	}

}
