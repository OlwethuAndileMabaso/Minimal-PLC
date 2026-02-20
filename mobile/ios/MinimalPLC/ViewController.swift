import UIKit
import WebKit

/// Main view controller — fullscreen WKWebView HMI kiosk for Minimal-PLC.
class ViewController: UIViewController, WKNavigationDelegate {

    // MARK: - Properties

    private var webView: WKWebView!
    private var activityIndicator: UIActivityIndicatorView!
    private let prefKey = "minimalplc_server_ip"
    private let defaultIP = "192.168.1.100:8080"

    // MARK: - Lifecycle

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = UIColor(red: 0.051, green: 0.067, blue: 0.09, alpha: 1)

        setupWebView()
        setupActivityIndicator()

        let serverIP = UserDefaults.standard.string(forKey: prefKey)
        if serverIP == nil || serverIP!.isEmpty {
            promptForServerIP()
        } else {
            loadHMI(serverIP: serverIP!)
        }
    }

    override var prefersStatusBarHidden: Bool { return true }

    override var supportedInterfaceOrientations: UIInterfaceOrientationMask {
        return .landscape
    }

    // MARK: - UI Setup

    private func setupWebView() {
        let config = WKWebViewConfiguration()
        config.allowsInlineMediaPlayback = true
        config.mediaTypesRequiringUserActionForPlayback = []

        webView = WKWebView(frame: .zero, configuration: config)
        webView.translatesAutoresizingMaskIntoConstraints = false
        webView.navigationDelegate = self
        webView.backgroundColor = UIColor.clear
        view.addSubview(webView)

        NSLayoutConstraint.activate([
            webView.topAnchor.constraint(equalTo: view.topAnchor),
            webView.bottomAnchor.constraint(equalTo: view.bottomAnchor),
            webView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            webView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
        ])
    }

    private func setupActivityIndicator() {
        if #available(iOS 13.0, *) {
            activityIndicator = UIActivityIndicatorView(style: .large)
            activityIndicator.color = UIColor(red: 0, green: 0.831, blue: 1, alpha: 1)
        } else {
            activityIndicator = UIActivityIndicatorView(style: .whiteLarge)
        }
        activityIndicator.translatesAutoresizingMaskIntoConstraints = false
        activityIndicator.hidesWhenStopped = true
        view.addSubview(activityIndicator)

        NSLayoutConstraint.activate([
            activityIndicator.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            activityIndicator.centerYAnchor.constraint(equalTo: view.centerYAnchor),
        ])
    }

    // MARK: - HMI Loading

    private func loadHMI(serverIP: String) {
        let urlString = "http://\(serverIP)/hmi/runtime"
        guard let url = URL(string: urlString) else {
            showErrorPage(message: "Invalid server address: \(serverIP)")
            return
        }
        webView.load(URLRequest(url: url))
    }

    private func showErrorPage(message: String) {
        let html = """
        <html>
        <body style="background:#0d1117;color:#e6edf3;font-family:sans-serif;
                     display:flex;align-items:center;justify-content:center;
                     height:100vh;margin:0;">
          <div style="text-align:center">
            <div style="font-size:4rem">⚡</div>
            <h2>Connecting to Minimal-PLC…</h2>
            <p style="color:#8b949e">\(message)</p>
          </div>
        </body>
        </html>
        """
        webView.loadHTMLString(html, baseURL: nil)
    }

    // MARK: - First-launch dialog

    private func promptForServerIP() {
        let alert = UIAlertController(
            title: "⚡ Minimal-PLC",
            message: "Enter the server IP address and port:",
            preferredStyle: .alert
        )
        alert.addTextField { tf in
            tf.placeholder = "192.168.1.100:8080"
            tf.text = self.defaultIP
            tf.keyboardType = .URL
            tf.autocorrectionType = .no
        }
        alert.addAction(UIAlertAction(title: "Connect", style: .default) { [weak self] _ in
            guard let self = self else { return }
            let ip = alert.textFields?.first?.text?.trimmingCharacters(in: .whitespaces) ?? self.defaultIP
            let serverIP = ip.isEmpty ? self.defaultIP : ip
            UserDefaults.standard.set(serverIP, forKey: self.prefKey)
            self.loadHMI(serverIP: serverIP)
        })
        alert.addAction(UIAlertAction(title: "Change Server", style: .destructive) { [weak self] _ in
            UserDefaults.standard.removeObject(forKey: self?.prefKey ?? "")
            self?.promptForServerIP()
        })
        present(alert, animated: true)
    }

    // MARK: - WKNavigationDelegate

    func webView(_ webView: WKWebView, didStartProvisionalNavigation navigation: WKNavigation!) {
        activityIndicator.startAnimating()
    }

    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        activityIndicator.stopAnimating()
    }

    func webView(_ webView: WKWebView,
                 didFailProvisionalNavigation navigation: WKNavigation!,
                 withError error: Error) {
        activityIndicator.stopAnimating()
        showErrorPage(message: error.localizedDescription)
    }

    func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
        activityIndicator.stopAnimating()
        showErrorPage(message: error.localizedDescription)
    }
}
