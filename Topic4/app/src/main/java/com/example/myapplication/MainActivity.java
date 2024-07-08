package com.example.myapplication;


import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.util.Log;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "MainActivity";
    private TextView tempTextView; //显示温度
    private Button searchButton; //搜索按钮
    private EditText addressEditText; // 输入框
    private ExecutorService executorService; // 线程池
    private Handler handler; // 处理器 更新UI


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // 设置布局文件
        setContentView(R.layout.activity_main);

        tempTextView = findViewById(R.id.tempTextView);
        searchButton = findViewById(R.id.searchButton);
        addressEditText = findViewById(R.id.addressEditText);

        // 初始化ExecutorService和handler，分别用于线程池和线程之间的信息传递
        executorService = Executors.newSingleThreadExecutor();
        handler = new Handler(Looper.getMainLooper());

        // 事件监听
        searchButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String address = addressEditText.getText().toString();
                if (!address.isEmpty()) {
                    fetchWeatherData(address);
                } else {
                    tempTextView.setText("请输入城市名称");
                }
            }
        });


    }

    // 获取天气数据
    private void fetchWeatherData(String address) {
        executorService.execute(new Runnable() {
            @Override
            public void run() {
                String apiKey = "4c3f77baf778c7ffa85e66c682c9ffc2";
                String urlString = "https://api.openweathermap.org/data/2.5/weather?q=" + address + "&appid=" + apiKey;
                try{
                    URL url = new URL(urlString);
                    HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
                    try{
                        BufferedReader reader = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
                        StringBuilder result = new StringBuilder();
                        String line;
                        while((line = reader.readLine())!=null){
                            result.append(line);
                        }
                        String response = result.toString();
                        Log.d(TAG, "Received response: " + response);

                        // 主线程更新UI
                        handler.post(new Runnable(){
                            @Override
                            public void run(){
                                updateUI(response);
                            }
                        });
                    }finally{
                        urlConnection.disconnect();
                    }
                }catch(Exception e){
                    e.printStackTrace();
                    Log.e(TAG, "Error fetching weather data", e);
                    handler.post(new Runnable(){
                        @Override
                        public void run(){
                            tempTextView.setText("查询失败");
                        }
                    });
                }
            }
        });

    }

    // 更新UI
    private void updateUI(String result){
        if(result!=null){
            try{
                JSONObject jsonObject = new JSONObject(result);
                if(jsonObject.has("main")){
                    JSONObject mainObject = jsonObject.getJSONObject("main");
                    double temp = mainObject.getDouble("temp") - 273.15;
                    tempTextView.setText(String.format("%.2f°C", temp));
                }
                else{
                    tempTextView.setText("查询不到此地的天气信息");
                }
            }catch(Exception e){
                e.printStackTrace();
                tempTextView.setText("解析失败");
            }
        }else{
            tempTextView.setText("查询失败");
        }
    }
}


