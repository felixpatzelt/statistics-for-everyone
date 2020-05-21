from IPython.display import SVG

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
        
        The data, url, filename and metadata arguments are passed to the SVG constructor.
        width and height should be strings containing valid values for
        the repsective html attributes. center=True adds a margin that will
        automatically center the div within its parent element.
        
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