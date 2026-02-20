import UIKit
import WebKit

class ViewController: UIViewController, WKNavigationDelegate {

    // Change this to your PLC runtime IP address or hostname
    private let runtimeURL = "http://192.168.1.100:8080"

    private var webView: WKWebView!

    override func viewDidLoad() {
        super.viewDidLoad()

        webView = WKWebView(frame: view.bounds)
        webView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        webView.navigationDelegate = self
        view.addSubview(webView)

        if let url = URL(string: runtimeURL) {
            webView.load(URLRequest(url: url))
        }
    }
}
