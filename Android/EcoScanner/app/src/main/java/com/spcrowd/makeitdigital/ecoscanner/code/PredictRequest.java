package com.spcrowd.makeitdigital.ecoscanner.code;

import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.view.View;
import android.widget.TextView;

import com.spcrowd.makeitdigital.ecoscanner.CameraActivity;
import com.spcrowd.makeitdigital.ecoscanner.PredictActivity;
import com.spcrowd.makeitdigital.ecoscanner.R;

import org.apache.commons.io.IOUtils;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;

/**
 * Created by Aliaksandr_Haurylik on 3/17/2018.
 */

public class PredictRequest extends AsyncTask<String, String, String> {
    private final static String ImageProcessorUrl = "http://epbyminw3809t1:3000/api/upload";

    private final String crlf = "\r\n";
    private final String twoHyphens = "--";
    private final String boundary =  "*****";
    private Activity activity;
    private final String attachmentName = "pic";
    private final String attachmentFileName = "pic.jpg";

    public PredictRequest(Activity activity){
        super();
        this.activity = activity;
    }

    @Override
    protected String doInBackground(String... strings) {
        try {
            File mFile = new File(this.activity.getExternalFilesDir(null), this.attachmentFileName);
            String resp = this.postImage(mFile.getPath());
            return resp;
        } catch (Exception e){
            return e.toString();
        }
    }

    @Override
    protected void onPostExecute(String result) {
        super.onPostExecute(result);
        PredictActivity predictActivity = (PredictActivity)this.activity;
        predictActivity.predictTxtStatus.setText(result);
        predictActivity.predictProgressBar.setVisibility(View.INVISIBLE);

        //Do anything with response..
    }

    public String postImage(String filepath) throws Exception {
        HttpURLConnection connection = null;
        DataOutputStream outputStream = null;
        InputStream inputStream = null;

        String twoHyphens = "--";
        String boundary =  "*****"+Long.toString(System.currentTimeMillis())+"*****";
        String lineEnd = "\r\n";

        int bytesRead, bytesAvailable, bufferSize;
        byte[] buffer;
        int maxBufferSize = 1*1024*1024;

        String filefield = "image";

        String[] q = filepath.split("/");
        int idx = q.length - 1;

        File file = new File(filepath);
        FileInputStream fileInputStream = new FileInputStream(file);

        URL url = new URL(this.ImageProcessorUrl);
        connection = (HttpURLConnection) url.openConnection();

        connection.setDoInput(true);
        connection.setDoOutput(true);
        connection.setUseCaches(false);

        connection.setRequestMethod("POST");
        connection.setRequestProperty("Connection", "Keep-Alive");
        connection.setRequestProperty("User-Agent", "Android Multipart HTTP Client 1.0");
        connection.setRequestProperty("Content-Type", "multipart/form-data; boundary="+boundary);

        outputStream = new DataOutputStream(connection.getOutputStream());
        outputStream.writeBytes(twoHyphens + boundary + lineEnd);
        outputStream.writeBytes("Content-Disposition: form-data; name=\"" + filefield + "\"; filename=\"" + q[idx] +"\"" + lineEnd);
        outputStream.writeBytes("Content-Type: image/jpeg" + lineEnd);
        outputStream.writeBytes("Content-Transfer-Encoding: binary" + lineEnd);
        outputStream.writeBytes(lineEnd);

        bytesAvailable = fileInputStream.available();
        bufferSize = Math.min(bytesAvailable, maxBufferSize);
        buffer = new byte[bufferSize];

        bytesRead = fileInputStream.read(buffer, 0, bufferSize);
        while(bytesRead > 0) {
            outputStream.write(buffer, 0, bufferSize);
            bytesAvailable = fileInputStream.available();
            bufferSize = Math.min(bytesAvailable, maxBufferSize);
            bytesRead = fileInputStream.read(buffer, 0, bufferSize);
        }

        outputStream.writeBytes(lineEnd);
        outputStream.writeBytes(twoHyphens + boundary + twoHyphens + lineEnd);

        inputStream = connection.getInputStream();

        int status = connection.getResponseCode();
        if (status == HttpURLConnection.HTTP_OK) {
            BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String inputLine;
            StringBuffer response = new StringBuffer();

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }

            inputStream.close();
            connection.disconnect();
            fileInputStream.close();
            outputStream.flush();
            outputStream.close();

            return response.toString();
        } else {
            throw new Exception("Non ok response returned");
        }
    }


}
