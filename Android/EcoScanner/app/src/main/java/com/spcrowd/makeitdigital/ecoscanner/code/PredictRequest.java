package com.spcrowd.makeitdigital.ecoscanner.code;

import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.widget.TextView;

import com.spcrowd.makeitdigital.ecoscanner.CameraActivity;
import com.spcrowd.makeitdigital.ecoscanner.PredictActivity;
import com.spcrowd.makeitdigital.ecoscanner.R;

import org.apache.commons.io.IOUtils;

import java.io.BufferedInputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

/**
 * Created by Aliaksandr_Haurylik on 3/17/2018.
 */

public class PredictRequest extends AsyncTask<String, String, String> {
    private final static String ImageProcessorUrl = "http://epbyminw3809t1:3000/health/predict";
    private Activity activity;

    public PredictRequest(Activity activity){
        super();
        this.activity = activity;
    }

    @Override
    protected String doInBackground(String... strings) {
        try {
            URL url = new URL(ImageProcessorUrl);
            HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
            try {
                InputStream in = new BufferedInputStream(urlConnection.getInputStream());
                String response = IOUtils.toString(in, StandardCharsets.UTF_8);
                return response;
            } catch (Exception e) {
                return e.toString();
            } finally {
                urlConnection.disconnect();
            }
        } catch (Exception e){
            return e.toString();
        }
    }

    @Override
    protected void onPostExecute(String result) {
        super.onPostExecute(result);
        OpenPredictActivity(this.activity, result);

        //Do anything with response..
    }

    public void OpenPredictActivity(Activity activity, String result){
        Intent intent = new Intent(activity.getApplicationContext(), PredictActivity.class);
        activity.startActivity(intent);
        TextView predictTxtStatus = activity.findViewById(R.id.predictTxtStatus);
        predictTxtStatus.setText(result);
    }
}
