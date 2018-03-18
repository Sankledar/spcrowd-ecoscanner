package com.spcrowd.makeitdigital.ecoscanner;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Adapter;
import android.widget.ArrayAdapter;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.ProgressBar;
import android.widget.TextView;

import com.spcrowd.makeitdigital.ecoscanner.code.ImageProcessor;

import java.util.ArrayList;

public class PredictActivity extends AppCompatActivity {
    public TextView predictTxtStatus = null;
    public ProgressBar predictProgressBar = null;
    public ListView predictListView = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_predict);
        predictTxtStatus = findViewById(R.id.predictTxtStatus);
        predictProgressBar = findViewById(R.id.predictProgressBar);
        predictListView = findViewById(R.id.predictListView);
        ImageProcessor.ProcessImage(this);
    }

    public void processPredictResponse(String result){
        this.predictTxtStatus.setText(result);
        //this.predictProgressBar.
        this.predictProgressBar.setVisibility(View.GONE);
        ArrayList arrayList = new ArrayList<String>();
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(getApplicationContext(), R.layout.predict_item, R.id.predictItemLabel, arrayList);
        this.predictListView.setAdapter(adapter);
        // this line adds the data of your EditText and puts in your array
        arrayList.add("Hello!");
        arrayList.add("Hello!2");
        arrayList.add("Hello!3");
        // next thing you have to do is check if your adapter has changed
        adapter.notifyDataSetChanged();
    }
}
