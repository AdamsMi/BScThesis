import UIKit

class ViewController: UIViewController, UITableViewDataSource, UITableViewDelegate, UITextFieldDelegate {

    // MARK: - Outlets
    
    @IBOutlet weak var newsTableView: UITableView!
    
    // MARK: - Properties
    
    var newsArray: [News]
    
    
    required init(coder aDecoder: NSCoder) {
        newsArray = []
        super.init(coder: aDecoder)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        registerNib()
        
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    // MARK: - TableView Methods
    
    private func registerNib() {
        let nibName = UINib(nibName: "NewsTableViewCell", bundle:nil)
        newsTableView.registerNib(nibName, forCellReuseIdentifier: NewsTableViewCell.cellIdentfier())
    }
    
    
    func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return self.newsArray.count
    }
    
    func tableView(tableView: UITableView, heightForRowAtIndexPath indexPath: NSIndexPath) -> CGFloat {
        return 71
    }
    
    func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        
        let cell = tableView.dequeueReusableCellWithIdentifier(
            NewsTableViewCell.cellIdentfier(), forIndexPath: indexPath) as! NewsTableViewCell
        
        let singleNews = newsArray[indexPath.row]
        cell.initWithNews(singleNews)
        
        return cell;
    }
    
    // MARK: - TextField Methods
    
    func textFieldShouldReturn(textField: UITextField) -> Bool {
        let queryText = textField.text
        textField.resignFirstResponder()
        
        searchResultsWithQuery(queryText)
        
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

