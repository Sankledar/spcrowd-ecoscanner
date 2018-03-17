package com.spcrowd.makeitdigital.ecoscanner.code;

import android.app.Activity;

import org.apache.commons.io.IOUtils;

import java.io.BufferedInputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

/**
 * Created by Aliaksandr_Haurylik on 3/17/2018.
 */

public final class ImageProcessor {
    private final static String ImageProcessorUrl = "http://epbyminw3809t1:3000/health/predict";

    public static void ProcessImage(Activity activity){
        PredictRequest pr = new PredictRequest(activity);
        pr.execute();
    }

}
