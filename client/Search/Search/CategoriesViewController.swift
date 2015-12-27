import UIKit

class CategoriesViewController: UIViewController {

    // Outlets
    @IBOutlet weak var categoriesCollectionView: UICollectionView!
    @IBOutlet weak var previousButton: UIButton!
    
    // Properties
    var clusteringData: ClusteringResponse?
    var path = [String]()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.initialCluster()
        
        let lpgr : UILongPressGestureRecognizer = UILongPressGestureRecognizer(target: self, action: "handleLongPress:")
        lpgr.minimumPressDuration = 0.5
        lpgr.delegate = self
        lpgr.delaysTouchesBegan = true
        self.categoriesCollectionView?.addGestureRecognizer(lpgr)
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    @IBAction func previousAction(sender: AnyObject) {
        
        path.removeLast()
        fadeOutCollectionView()
        
        if path.count == 0 {
            changeButtonToChooseCategory()
            initialCluster()
        } else {
            let lastItem = path.last!
            path.removeLast()
            clusterForIndex(Int(lastItem)!)
        }
        
        
    }
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        if segue.identifier == "news_segue" {
            let destVC = segue.destinationViewController as! SearchViewController
            path.append("\(sender!)")
            destVC.clusterPath = path
            path.removeLast()
        }
    }
    
    // MARK: - Customize view
    
    private func changeButtonToPrevious() {
        previousButton.enabled = true
        previousButton.setTitle("Previous", forState: .Normal)
    }
    
    
    private func changeButtonToChooseCategory() {
        previousButton.enabled = false
        previousButton.setTitle("Choose category you are intrested in", forState: .Normal)
    }
    
    private func fadeOutCollectionView() {
        UIView.transitionWithView(categoriesCollectionView,
            duration: 0.4,
            options: .TransitionCrossDissolve,
            animations: { () -> Void in
                self.categoriesCollectionView.alpha = 0.0
            }, completion: nil)
    }
    
    private func fadeInCollectionView() {
        
        UIView.transitionWithView(categoriesCollectionView,
            duration: 0.4,
            options: .TransitionCrossDissolve,
            animations: { () -> Void in
                self.categoriesCollectionView.alpha = 1.0
            }, completion: nil)
    }
    
    // MARK: - API Calls
    
    private func initialCluster() {
        
        UIApplication.sharedApplication().networkActivityIndicatorVisible = true
        ClusteringMethod.initialClustering { (result) -> () in
            UIApplication.sharedApplication().networkActivityIndicatorVisible = false
            self.clusteringData = result
            self.categoriesCollectionView.reloadData()
            self.fadeInCollectionView()
        }
    }
    
    private func clusterForIndex(index: Int) {
        path.append("\(index)")
        
        UIApplication.sharedApplication().networkActivityIndicatorVisible = true
        ClusteringMethod.clusterForPath(path) { (result) -> () in
            
            UIApplication.sharedApplication().networkActivityIndicatorVisible = false
            self.clusteringData = result
            self.categoriesCollectionView.reloadData()
            self.fadeInCollectionView()
        }
    }


}

extension CategoriesViewController: UICollectionViewDelegate, UICollectionViewDataSource, UIGestureRecognizerDelegate {
    
    func handleLongPress(gestureRecognizer : UILongPressGestureRecognizer){
        
        if (gestureRecognizer.state != UIGestureRecognizerState.Ended){
            return
        }
        
        let p = gestureRecognizer.locationInView(self.categoriesCollectionView)
        
        if let indexPath : NSIndexPath = (self.categoriesCollectionView?.indexPathForItemAtPoint(p))!{
            
            self.performSegueWithIdentifier("news_segue", sender: indexPath.row)
            
        }
        
    }
    
    func collectionView(collectionView: UICollectionView, didSelectItemAtIndexPath indexPath: NSIndexPath) {
        
        if let intense = clusteringData?.clusters?["\(indexPath.row)"] {
            if intense<=12 {
                return
            }
        }
        
        changeButtonToPrevious()
        fadeOutCollectionView()
        clusterForIndex(indexPath.row)
    }
    
    func collectionView(collectionView: UICollectionView, cellForItemAtIndexPath indexPath: NSIndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCellWithReuseIdentifier(CategoryCollectionViewCell.cellName, forIndexPath: indexPath) as! CategoryCollectionViewCell
        
        var categoryName = ""
        var categoriesAvalible = false
        
        if let categories = clusteringData?.categories?["\(indexPath.row)"] {
            categoryName += categoryFromStrings(categories, newLine: false) + "\n"
            categoriesAvalible = true
        }
        if let words = clusteringData?.freqWords?["\(indexPath.row)"] {
            categoryName += categoryFromStrings(words, newLine: !categoriesAvalible)
        }
        cell.categoryNameLabel.text = categoryName
        if let intense = clusteringData?.clusters?["\(indexPath.row)"] {
            cell.backgroundColor = UIColor(red: 0.6, green: 0.34, blue: 0.71, alpha: CGFloat(intense)/120.0)
        } else {
            cell.backgroundColor = UIColor.clearColor()
        }
        
        return cell
    }
    
    func collectionView(collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        if clusteringData?.freqWords?.count>0
            || clusteringData?.categories?.count>0 {
            return 12
        }
        return 0
    }
    
    private func categoryFromStrings(strings: [String], newLine:Bool = true) -> String {
        
        var firstCategory = true
        var result = ""
        
        for category in strings {
            
            if category.characters.count > 2 {
                if !firstCategory {
                    result += (newLine ? "\n" : ", ")
                } else {
                    firstCategory = false
                }
            
                result += category.stringByReplacingOccurrencesOfString(
                    "/", withString: (newLine ? "\n" : ", "))
            }
        }

        return result
        
    }
    
}