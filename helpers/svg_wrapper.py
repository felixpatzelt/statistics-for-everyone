"""SVGWrapper improves on IPython's SVG class."""
from IPython.display import SVG
from shutil import copyfile
import os

class SVGWrapper():
    def __init__(
            self, 
            data=None, 
            url=None, 
            filename=None, 
            metadata=None, 
            width='100%',
            height='100%',
            center=True
        ):
        """
        Allow to set the width and height of a IPython.display.SVG
        by wrapping it in a <div> tag.
        
        The data, url, filename and metadata arguments are passed to the SVG 
        constructor. width and height should be strings containing valid values 
        for the repsective html attributes. center=True adds a margin that will
        automatically center the div within its parent element.
        
        Because the SVG is embedded in the DOM, it is accessible to other 
        stylesheets. This can lead to more flexibility, but also to conflicts
        e.g. with transformations.
        
        Example:
            SVGWrapper('path/to/file.svg', width='50%', height='50%')
        """
        self.svg = SVG(data=data, url=url, filename=filename, metadata=metadata)
        self.width = width
        self.height = height
        self.center = center
        
    def _repr_html_(self):
        divstyle = f"width: {self.width}; height: {self.height};"
        if self.center:
            divstyle += " margin: auto;"
        html = f"""
            <div style="{divstyle}">
                {self.svg._repr_svg_()}
            </div>
        """
        return html
        
        
class SVGImg():
    def __init__(
            self, 
            url, 
            width='100%',
            height='100%',
            center=False,
            output_dir=None
        ):
        """
        Link SVG as <img>. 
        
        Optionally copy to output_dir/url for later serving with same relative
        path.
        
        Example:
            SVGImg('path/to/file.svg', width='50%', height='50%')
        """
        self.url = url
        self.width = width
        self.height = height
        self.center = center
        if output_dir is not None:
            output_url = os.path.join(output_dir, url)
            os.makedirs(os.path.dirname(output_url), exist_ok=True)
            copyfile(url, output_url)

        
    def _repr_html_(self):
        style = f"width: {self.width}; height: {self.height};"
        if self.center:
            style += " margin: auto;"
        html = f"""<img src="{self.url}" width="{self.width}" height="{self.height}"></img>"""
        if os.environ.get('CONVERT') == 'TRUE':
            html = f"""
                <object type="image/svg+xml" data="{self.url}" style="{style}">
                    {html}
                </object>
                """
            
        return html