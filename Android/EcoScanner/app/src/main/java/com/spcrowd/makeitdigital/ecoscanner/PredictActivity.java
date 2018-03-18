package com.spcrowd.makeitdigital.ecoscanner;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.ProgressBar;
import android.widget.TextView;

import com.spcrowd.makeitdigital.ecoscanner.code.ImageProcessor;

public class PredictActivity extends AppCompatActivity {
    public TextView predictTxtStatus = null;
    public ProgressBar predictProgressBar = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_predict);
        predictTxtStatus = findViewById(R.id.predictTxtStatus);
        predictProgressBar = findViewById(R.id.predictProgressBar);
        ImageProcessor.ProcessImage(this);
    }
}
