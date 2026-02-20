package com.minimalplc.app;

import android.app.AlertDialog;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.View;
import android.view.WindowManager;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.EditText;
import android.widget.ProgressBar;
import androidx.appcompat.app.AppCompatActivity;

/**
 * MainActivity for Minimal-PLC Android HMI viewer.
 *
 * <p>Displays the HMI runtime (/hmi/runtime) in a fullscreen WebView.
 * On first launch an AlertDialog prompts the user for the server IP:port.</p>
 */
public class MainActivity extends AppCompatActivity {

    private static final String PREF_FILE   = "MinimalPLC";
    private static final String PREF_SERVER = "server_ip";
    private static final String DEFAULT_IP  = "192.168.1.100:8080";

    private WebView     mWebView;
    private ProgressBar mProgress;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Fullscreen + keep screen on
        getWindow().addFlags(
            WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON |
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        );

        setContentView(R.layout.activity_main);

        mWebView  = findViewById(R.id.webView);
        mProgress = findViewById(R.id.progressBar);

        configureWebView();

        SharedPreferences prefs = getSharedPreferences(PREF_FILE, MODE_PRIVATE);
        String serverIp = prefs.getString(PREF_SERVER, null);

        if (serverIp == null || serverIp.isEmpty()) {
            promptForServerIp(prefs);
        } else {
            loadHmi(serverIp);
        }
    }

    // ── WebView configuration ───────────────────────────────────────────

    private void configureWebView() {
        WebSettings settings = mWebView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setLoadWithOverviewMode(true);
        settings.setUseWideViewPort(true);
        settings.setCacheMode(WebSettings.LOAD_DEFAULT);

        mWebView.setWebChromeClient(new WebChromeClient());
        mWebView.setWebViewClient(new WebViewClient() {

            @Override
            public void onPageStarted(WebView view, String url, Bitmap favicon) {
                mProgress.setVisibility(View.VISIBLE);
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                mProgress.setVisibility(View.GONE);
            }

            @Override
            public void onReceivedError(WebView view, WebResourceRequest request,
                                        WebResourceError error) {
                if (request.isForMainFrame()) {
                    view.loadData(
                        "<html><body style='background:#0d1117;color:#e6edf3;"
                        + "font-family:sans-serif;display:flex;align-items:center;"
                        + "justify-content:center;height:100vh;margin:0;'>"
                        + "<div style='text-align:center'>"
                        + "<div style='font-size:3rem'>⚡</div>"
                        + "<h2>Connecting to Minimal-PLC…</h2>"
                        + "<p style='color:#8b949e'>Make sure the server is running<br>"
                        + "and your device is on the same network.</p>"
                        + "</div></body></html>",
                        "text/html", "UTF-8"
                    );
                }
            }
        });
    }

    // ── Load HMI ────────────────────────────────────────────────────────

    private void loadHmi(String serverIp) {
        String url = "http://" + serverIp + "/hmi/runtime";
        mWebView.loadUrl(url);
    }

    // ── First-launch dialog ─────────────────────────────────────────────

    private void promptForServerIp(SharedPreferences prefs) {
        final EditText input = new EditText(this);
        input.setText(DEFAULT_IP);
        input.setHint("192.168.1.100:8080");

        new AlertDialog.Builder(this)
            .setTitle("⚡ Minimal-PLC")
            .setMessage("Enter the server IP address and port:")
            .setView(input)
            .setCancelable(false)
            .setPositiveButton("Connect", (dialog, which) -> {
                String ip = input.getText().toString().trim();
                if (ip.isEmpty()) ip = DEFAULT_IP;
                prefs.edit().putString(PREF_SERVER, ip).apply();
                loadHmi(ip);
            })
            .setNeutralButton("Change Server", (dialog, which) -> {
                prefs.edit().remove(PREF_SERVER).apply();
                promptForServerIp(prefs);
            })
            .show();
    }

    // ── Back button navigates WebView history ────────────────────────────

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK && mWebView.canGoBack()) {
            mWebView.goBack();
            return true;
        }
        return super.onKeyDown(keyCode, event);
    }
}
