import UIKit

extension UIView {
    
    class func loadFromNibNamed(nibNamed: String, bundle : NSBundle? = nil) -> UIView? {
        return UINib(
            nibName: nibNamed,
            bundle: bundle
            ).instantiateWithOwner(nil, options: nil)[0] as? UIView
    }
    
    @IBInspectable var cornerRadius: CGFloat {
        get {
            return layer.cornerRadius
        }
        set {
            layer.cornerRadius = newValue
            layer.masksToBounds = newValue > 0
        }
    }
    
    @IBInspectable var borderWidth: CGFloat {
        get {
            return layer.borderWidth
        }
        set {
            layer.borderWidth = newValue
        }
    }
    
    @IBInspectable var borderColor: UIColor {
        get {
            if let color = layer.borderColor {
                return UIColor(CGColor: color)
            } else {
                return UIColor.clearColor()
            }
        }
        set {
            layer.borderColor = newValue.CGColor
        }
    }
}

@IBDesignable
class FormTextField: UITextField {
    
    
    @IBInspectable var leftPadding: CGFloat {
        get {
            return 0
        }
        set {
            let paddingView = UIView(frame: CGRectMake(0, 0, newValue, 1))
            paddingView.backgroundColor = UIColor.clearColor()
            self.leftView = paddingView;
            self.leftViewMode = UITextFieldViewMode.Always;
        }
    }
    
    required init?(coder aDecoder: NSCoder) {
        super.init(coder: aDecoder)
        self.leftPadding = 10
        self.cornerRadius = 2.0;
    }
    
    override init(frame: CGRect) {
        super.init(frame: frame)
        self.leftPadding = 10
        self.cornerRadius = 2.0;
    }
    
}