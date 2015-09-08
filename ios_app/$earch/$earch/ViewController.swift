import UIKit

class ViewController: UIViewController, UITableViewDataSource, UITableViewDelegate {

    // MARK: - Outlets
    
    @IBOutlet weak var newsTableView: UITableView!
    
    // MARK: - Properties
    
    var newsArray: [News]?
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        registerNib()
        newsArray = NewsGenerator.generateNews()
        
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    // MARK: - TableView Methods
    
    private func registerNib() {
        let nibName = UINib(nibName: "NewsTableViewCell", bundle:nil)
        self.newsTableView.registerNib(nibName, forCellReuseIdentifier: NewsTableViewCell.cellIdentfier())
    }
    
    
    func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return 30;
    }
    
    func tableView(tableView: UITableView, heightForRowAtIndexPath indexPath: NSIndexPath) -> CGFloat {
        return 71;
    }
    
    func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        
        let cell = tableView.dequeueReusableCellWithIdentifier(
            NewsTableViewCell.cellIdentfier(), forIndexPath: indexPath) as! NewsTableViewCell
        
        if let news = self.newsArray {
            let singleNews = news[indexPath.row]
            cell.initWithNews(singleNews)
        }
        
        return cell;
    }

}

