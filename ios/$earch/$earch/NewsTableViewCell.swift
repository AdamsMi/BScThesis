import UIKit

class NewsTableViewCell: UITableViewCell {

    @IBOutlet weak var newsTitleLabel: UILabel!
    
    @IBOutlet weak var newsImageView: UIImageView!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)
    }
    
    class func cellIdentfier() -> String {
        return "NewsTableCell";
    }
    
    func initWithNews(news: News) {
        self.newsTitleLabel.text = news.title
        
        switch (news.provider) {
        case .ZERO_HEDGE:
            self.newsImageView.image = UIImage(named: "zerohedge")
            break
        case .THE_STREET:
            self.newsImageView.image = UIImage(named: "thestreet")
            break
        case .THE_TELEGRAPH:
            self.newsImageView.image = UIImage(named: "thetelegraph")
            break
        case .ROUTERS:
            self.newsImageView.image = UIImage(named: "routers")
            break
        case .UNDEFINED:
            break
        }
    }
    
    
}
