package com.spcrowd.makeitdigital.ecoscanner;

import android.app.Activity;
import android.content.Intent;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
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

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;

public class PredictActivity extends AppCompatActivity {
    //public TextView predictTxtStatus = null;
    public ProgressBar predictProgressBar = null;
    public ListView predictListView = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_predict);
        //predictTxtStatus = findViewById(R.id.predictTxtStatus);
        predictProgressBar = findViewById(R.id.predictProgressBar);
        predictListView = findViewById(R.id.predictListView);
        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        final Activity currentActivity = this;
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                OpenCameraActivity(currentActivity);
            }
        });
        ImageProcessor.ProcessImage(this);
    }

    public void OpenCameraActivity(Activity activity){
        Intent intent = new Intent(activity.getApplicationContext(), CameraActivity.class);
        activity.startActivity(intent);
    }

    public void processPredictResponse(String result){
        //this.predictTxtStatus.setText(result);
        //this.predictProgressBar.
        this.predictProgressBar.setVisibility(View.GONE);
        ArrayList arrayList = new ArrayList<String>();
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(getApplicationContext(), R.layout.predict_item, R.id.predictItemLabel, arrayList);
        this.predictListView.setAdapter(adapter);
        // this line adds the data of your EditText and puts in your array
        String jsonResult = ProcessJSon(result);
        arrayList.add(jsonResult);
        //arrayList.add("Hello!2");
        //arrayList.add("Hello!3");
        // next thing you have to do is check if your adapter has changed
        adapter.notifyDataSetChanged();
    }
    final  static  String messageYes = "Recyclable plastic: ";
    final  static  String messageNo = "Non recyclable plastic: ";

    public String ProcessJSon(String result){
        try {
            JSONObject json = new JSONObject(result);
            String predictStr = json.getString("predict");
            String predictProbaStr = json.getString("predict_proba");
            JSONArray predictStrArray = new JSONArray(predictStr);
            JSONArray predictProbaStrArray = new JSONArray(predictProbaStr);
            int predict = predictStrArray.getInt(0);
            double predictProba = predictProbaStrArray.getDouble(0);
            System.out.print("Predict=" + predict);
            System.out.print("Predict Probe=" + predictProba);
            String res = (predict == 1 ? messageYes : messageNo )+ (predictProba *100)+ "%";
            return res;
        } catch (Exception ex){
            return ex.toString();
        }
    }
}
