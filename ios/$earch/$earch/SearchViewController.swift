import UIKit

class SearchViewController: UIViewController {

    // MARK: - Outlets
    
    @IBOutlet weak var newsTableView: UITableView!
    @IBOutlet weak var searchTextFiedVerticalSpaceConstraint: NSLayoutConstraint!
    
    // MARK: - Properties
    
    var newsArray: [News]
    
    required init?(coder aDecoder: NSCoder) {
        newsArray = []
        super.init(coder: aDecoder)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
}

// MARK: - TableView Methods

extension SearchViewController: UITableViewDataSource, UITableViewDelegate {
    
    func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return self.newsArray.count
    }
    
    func tableView(tableView: UITableView, heightForRowAtIndexPath indexPath: NSIndexPath) -> CGFloat {
        return 71
    }
    
    func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        
        let cell = tableView.dequeueReusableCellWithIdentifier(
            NewsTableViewCell.cellName, forIndexPath: indexPath) as! NewsTableViewCell
        
        let singleNews = newsArray[indexPath.row]
        cell.initWithNews(singleNews)
        
        return cell;
    }
    
    func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
        let news = newsArray[indexPath.row] as News
        UIApplication.sharedApplication().openURL(news.url)
    }
    
}

extension SearchViewController: UITextFieldDelegate {

    // MARK: - TextField Methods
    
    func textFieldShouldReturn(textField: UITextField) -> Bool {
        if let queryText = textField.text {
            textField.resignFirstResponder()
            searchResultsWithQuery(queryText)
        }
        return true;
    }
    
    // MARK: - API Methods
    
    private func searchResultsWithQuery(query: String) {
        
        SearchMethod.searchWithString(query: query) { (response) -> () in
            if response.isResponseOK() {
                self.newsArray = response.newsArray
                self.newsTableView.reloadData()
            }
        }
        
    }
    
}

