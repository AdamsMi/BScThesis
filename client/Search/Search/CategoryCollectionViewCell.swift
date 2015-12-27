import UIKit

class CategoryCollectionViewCell: UICollectionViewCell {
    
    class var cellName: String {
        get {
            return "CategoryCollectionViewCell"
        }
    }
    
    @IBOutlet weak var categoryNameLabel: UILabel!
    
}
