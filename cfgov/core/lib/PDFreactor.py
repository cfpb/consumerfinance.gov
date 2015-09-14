"""This is the PDFreactor 6.3 Python API 
RealObjects(R) PDFreactor(R) is a powerful formatting processor for converting HTML and XML documents
into PDF.
 
The simplest sample for the PDFreactor Python API:
 
#!/usr/bin/python
from PDFreactor import *
pdfReactor = PDFreactor()
result = pdfReactor.renderDocumentFromURL("http://www.realobjects.com")
print "Content-Type: application/pdf"
print result
"""
import urllib
import urllib2
import binascii
import cgi
from xml.dom import minidom

class PDFreactor:
    #======================================#
    # Cleanup constants                    #
    #======================================#
    
    # Indicates that no cleanup will be performed when loading document.
    CLEANUP_NONE = 0
    
    # Indicates that JTidy will be used to perform a cleanup when loading a document.
    CLEANUP_JTIDY = 1
    
    # Indicates that the CyberNeko HTML parser will be used to perform a 
    # cleanup when loading a document.
    CLEANUP_CYBERNEKO = 2
    
    # Indicates that the TagSoup HTML parser will be used to perform a 
    # cleanup when loading a document.
    CLEANUP_TAGSOUP = 3
    
    # The default cleanup setting.
    CLEANUP_DEFAULT = CLEANUP_CYBERNEKO
    
    #=========================
    # Document type constants
    #=========================
    
    # Indicates that the document type will be detected automatically.
    #
    # A document has the type DOCTYPE_HTML5 if the name of the root element
    # is "html" (ignoring case considerations). In all other cases the
    # document type is DOCTYPE_XML.
     
    DOCTYPE_AUTODETECT = 0
    
    # Indicates that the document type will be set to generic XML.
    #
    # No default style sheet is used and the document is loaded as is without regards to style elements or
    # attributes.
     
    DOCTYPE_XML = 1
    
    # Indicates that the document type will be set to XHTML.
    #
    # The HTML default style sheet is used and the document is loaded regarding style elements, style
    # attributes and link stylesheets.
     
    DOCTYPE_XHTML = 2
    
    # Indicates that the document type will be set to HTML5.
    #
    # The HTML default style sheet is used and the document is loaded regarding style elements, style
    # attributes and link stylesheets.

    DOCTYPE_HTML5 = 3;
    
    # The default document type setting.
    #    
    # It is set to DOCTYPE_AUTODETECT.
     
    DOCTYPE_DEFAULT = DOCTYPE_AUTODETECT
    
    # ===================================
    # Document default language constant
    # ===================================
    
    # Indicates the Default language used for a document
    # if no other language is set in the document itself. 
    
    DOCUMENT_DEFAULT_LANGUAGE_DEFAULT = None
    
    #======================
    # Encryption constants
    #======================
    
    # Indicates that the document will not be encrypted.
    #     
    # If encryption is disabled then no user password and no owner password can be used.
     
    ENCRYPTION_NONE = 0
    
    # Indicates that the document will be encrypted using 40 bit encryption.
     
    ENCRYPTION_40 = 1
    
    # Indicates that the document will be encrypted using 128 bit encryption.
    #    
    # For normal purposes this value should be used.
     
    ENCRYPTION_128 = 2
    
    # The default encryption setting.    
    #
    # It is set to ENCRYPTION_NONE.
     
    ENCRYPTION_DEFAULT = ENCRYPTION_NONE
    
    #=====================
    # Log level constants
    #=====================
    
    # Indicates that no log events will be logged.
    #
    # see setLogLevel(int)
    LOG_LEVEL_NONE = 4
    
    # Indicates that only fatal log events will be logged.
    #
    # see setLogLevel(int)
    LOG_LEVEL_FATAL = 3
    
    # Indicates that warn and fatal log events will be logged.
    #
    # see setLogLevel(int)
    LOG_LEVEL_WARN = 2
    
    # Indicates that info, warn and fatal log events will be logged.
    #
    # see setLogLevel(int)
    LOG_LEVEL_INFO = 1
    
    # Indicates that debug, info, warn and fatal log events will be logged.
    #
    # see setLogLevel(int)
    LOG_LEVEL_DEBUG = 0
    
    # Indicates that all log events will be logged.
    #
    # see setLogLevel(int)
    LOG_LEVEL_PERFORMANCE = -1
    
    # The default log level setting. It is set to 'LOG_LEVEL_NONE'.
    #
    # see setLogLevel(int)
    LOG_LEVEL_DEFAULT = LOG_LEVEL_NONE
    
    #===================
    # Viewerpreferences 
    #===================  
      
       
    # Display one page at a time. (default)
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_PAGE_LAYOUT_SINGLE_PAGE = 1
    
    # Display the pages in one column.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_PAGE_LAYOUT_ONE_COLUMN = 1 << 1
      
    # Display the pages in two columns, with odd numbered pages on the left.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_PAGE_LAYOUT_TWO_COLUMN_LEFT = 1 << 2
      
    # Display the pages in two columns, with odd numbered pages on the right.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_PAGE_LAYOUT_TWO_COLUMN_RIGHT = 1 << 3
       
    # Display two pages at a time, with odd numbered pages on the left.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_PAGE_LAYOUT_TWO_PAGE_LEFT = 1 << 4
       
    # Display two pages at a time, with odd numbered pages on the right.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_PAGE_LAYOUT_TWO_PAGE_RIGHT = 1 << 5
       
    # Show no panel on startup.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_PAGE_MODE_USE_NONE = 1 << 6
       
    # Show document outline panel on startup.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_PAGE_MODE_USE_OUTLINES = 1 << 7
      
    # Show thumbnail images panel on startup.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_PAGE_MODE_USE_THUMBS = 1 << 8
      
    # Switch to fullscreen mode on startup.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_PAGE_MODE_FULLSCREEN = 1 << 9
      
    # Show optional content group panel on startup.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_PAGE_MODE_USE_OC = 1 << 10
      
    # Show attachments panel on startup.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_PAGE_MODE_USE_ATTACHMENTS = 1 << 11
      
    # Hide the viewer application's tool bars when the document is active.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_HIDE_TOOLBAR = 1 << 12
      
    # Hide the viewer application's menu bar when the document is active.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_HIDE_MENUBAR = 1 << 13
      
    # Hide user interface elements in the document's window.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_HIDE_WINDOW_UI = 1 << 14
      
    # Resize the document's window to fit the size of the first displayed page.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_FIT_WINDOW = 1 << 15
      
    # Position the document's window in the center of the screen.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_CENTER_WINDOW = 1 << 16
      
    # Display the document's title in the top bar.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_DISPLAY_DOC_TITLE = 1 << 17
      
    # Show document outline panel on exiting full-screen mode.
    # Has to be combined with 'VIEWER_PREFERENCES_PAGE_MODE_FULLSCREEN'.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_NON_FULLSCREEN_PAGE_MODE_USE_NONE = 1 << 18
       
    # Show thumbnail images panel on exiting full-screen mode.
    # Has to be combined with 'VIEWER_PREFERENCES_PAGE_MODE_FULLSCREEN'.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_NON_FULLSCREEN_PAGE_MODE_USE_OUTLINES = 1 << 19
       
    # Show optional content group panel on exiting full-screen mode.
    # Has to be combined with 'VIEWER_PREFERENCES_PAGE_MODE_FULLSCREEN'.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_NON_FULLSCREEN_PAGE_MODE_USE_THUMBS = 1 << 20
       
    # Show attachments panel on exiting full-screen mode.
    # Has to be combined with 'VIEWER_PREFERENCES_PAGE_MODE_FULLSCREEN'.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_NON_FULLSCREEN_PAGE_MODE_USE_OC = 1 << 21
     
    # Position pages in ascending order from left to right.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_DIRECTION_L2R = 1 << 22
       
    # Position pages in ascending order from right to left.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_DIRECTION_R2L = 1 << 23
    
    # Print dialog default setting: disabled scaling.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_PRINTSCALING_NONE = 1 << 24
    
    # Print dialog default setting: set scaling to application default value.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_PRINTSCALING_APPDEFAULT = 1 << 25
    
    # Print dialog default setting: simplex.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_DUPLEX_SIMPLEX = 1 << 26
    
    # Print dialog default setting: duplex (short edge).
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_DUPLEX_FLIP_SHORT_EDGE = 1 << 27
    
    # Print dialog default setting: duplex (long edge).
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_DUPLEX_FLIP_LONG_EDGE = 1 << 28
    
    # Print dialog default setting: do not pick tray by PDF size.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_PICKTRAYBYPDFSIZE_FALSE = 1 << 29
    
    # Print dialog default setting: pick tray by PDF size.
    #
    # see setViewerPreferences(int)
    VIEWER_PREFERENCES_PICKTRAYBYPDFSIZE_TRUE = 1 << 30
    
    # Processing preferences flag for the memory saving mode for images.
    #
    # see setProcessingPreferences(int)
    PROCESSING_PREFERENCES_SAVE_MEMORY_IMAGES = 1
    
    #The color space RGB.
    COLOR_SPACE_RGB = 0

    #The color space CMYK.
    COLOR_SPACE_CMYK = 1
    
    # =======================
    # Conformance constants
    # =======================
    
    # PDF with no additional restrictions (default).
    #
    # setConformance(int)
    CONFORMANCE_PDF = 0
    
    # PDF/A-1a (ISO 19005-1 Level A).
    #
    # setConformance(int)
    CONFORMANCE_PDFA = 1
    
    # The default value of the conformance property which is 'CONFORMANCE_PDF'.
    #
    # setConformance(int)
    CONFORMANCE_DEFAULT = CONFORMANCE_PDF
    
    # =================================
    # Processing Preferences Constants
    # =================================
    
    # Processing preferences flag for the memory saving mode for images
    PROCESSING_PREFERENCES_SAVE_MEMORY_IMAGES = 1
    
    #=================================
    # Exceeding Content Constants
    #=================================
    
    # Do not log exceeding content.
    #
    # setLogExceedingContent(int, int)
    EXCEEDING_CONTENT_ANALYZE_NONE = 0
    
    # Log exceeding content.
    #
    # setLogExceedingContent(int, int)
    EXCEEDING_CONTENT_ANALYZE_CONTENT = 1
    
    # Log exceeding content and boxes without absolute positioning.
    #
    # setLogExceedingContent(int, int)
    EXCEEDING_CONTENT_ANALYZE_CONTENT_AND_STATIC_BOXES = 2
    
    # Log exceeding content and all boxes.
    #
    # setLogExceedingContent(int, int)
    EXCEEDING_CONTENT_ANALYZE_CONTENT_AND_BOXES = 3
    
    # Do not log exceeding content.
    #
    # setLogExceedingContent(int, int)
    EXCEEDING_CONTENT_AGAINST_NONE = 0
    
    # Log content exceeding the edges of its page.
    #
    # setLogExceedingContent(int, int)
    EXCEEDING_CONTENT_AGAINST_PAGE_BORDERS = 1
    
    # Log content exceeding its page content area (overlaps the page margin).
    #
    # setLogExceedingContent(int, int)
    EXCEEDING_CONTENT_AGAINST_PAGE_CONTENT = 2
    
    # Log content exceeding its container.
    #
    # setLogExceedingContent(int, int)
    EXCEEDING_CONTENT_AGAINST_PARENT = 3
    
    #=================================
    # Overlay & Merge Constants
    #=================================
    
    # Default merge mode: Append converted document to existing PDF.
    #
    # see setMergeMode(int)
    MERGE_MODE_APPEND = 1
    
    # Alternate merge mode: Prepend converted document to existing PDF.
    #
    # see setMergeMode(int)
    MERGE_MODE_PREPEND = 2
    
    # Alternate merge mode (overlay): Adding converted document above the existing PDF.
    #
    # see setMergeMode(int)
    MERGE_MODE_OVERLAY = 3
    
    # Alternate merge mode (overlay): Adding converted document below the existing PDF.
    #
    # see setMergeMode(int)
    MERGE_MODE_OVERLAY_BELOW = 4
    
    # No pages of the shorter document are repeated, leaving some pages of the longer document without overlay.
    #
    # setOverlayRepeat(int)
    OVERLAY_REPEAT_NONE = 0
    
    # Last page of the shorter document is repeated, to overlay all pages of the longer document.
    #
    # setOverlayRepeat(int)
    OVERLAY_REPEAT_LAST_PAGE = 1
    
    # All pages of the shorter document are repeated, to overlay all pages of the longer document.
    #
    # setOverlayRepeat(int)
    OVERLAY_REPEAT_ALL_PAGES = 2
    
    #=================================
    # Multipage & Order Constants
    #=================================
    
    # Arranges the pages on a sheet from left to right and top to bottom.
    #
    # see setPagesPerSheetProperties(int, int, string, string, string, int)
    PAGES_PER_SHEET_DIRECTION_RIGHT_DOWN = 0
    
    # Arranges the pages on a sheet from right to left and top to bottom.
    #
    # see setPagesPerSheetProperties(int, int, string, string, string, int)
    PAGES_PER_SHEET_DIRECTION_LEFT_DOWN = 1
    
    # Arranges the pages on a sheet from left to right and bottom to top.
    #
    # see setPagesPerSheetProperties(int, int, string, string, string, int)
    PAGES_PER_SHEET_DIRECTION_RIGHT_UP = 2
    
    # Arranges the pages on a sheet from right to left and bottom to top.
    #
    # see setPagesPerSheetProperties(int, int, string, string, string, int)
    PAGES_PER_SHEET_DIRECTION_LEFT_UP = 3
    
    # Arranges the pages on a sheet from top to bottom and left to right.
    #
    # see setPagesPerSheetProperties(int, int, string, string, string, int)
    PAGES_PER_SHEET_DIRECTION_DOWN_RIGHT = 4
    
    # Arranges the pages on a sheet from top to bottom and right to left.
    #
    # see setPagesPerSheetProperties(int, int, string, string, string, int)
    PAGES_PER_SHEET_DIRECTION_DOWN_LEFT = 5
    
    # Arranges the pages on a sheet from bottom to top and left to right.
    #
    # see setPagesPerSheetProperties(int, int, string, string, string, int)
    PAGES_PER_SHEET_DIRECTION_UP_RIGHT = 6
    
    # Arranges the pages on a sheet from bottom to top and right to left.
    #
    # see setPagesPerSheetProperties(int, int, string, string, string, int)
    PAGES_PER_SHEET_DIRECTION_UP_LEFT = 7
    
    # Page order mode to reverse the page order.
    #
    # see setPageOrder(string)
    PAGE_ORDER_REVERSE = "REVERSE"
    
    # Page order mode to keep odd pages only.
    #
    # see setPageOrder(string)
    PAGE_ORDER_ODD = "ODD"
    
    # Page order mode to keep even pages only.
    #
    # see setPageOrder(string)
    PAGE_ORDER_EVEN = "EVEN"
    
    # Page order mode to arrange all pages in booklet order.
    #
    # see setPageOrder(string)
    PAGE_ORDER_BOOKLET = "BOOKLET"
    
    # Page order mode to arrange all pages in right-to-left booklet order.
    #
    # see setPageOrder(string)
    PAGE_ORDER_BOOKLET_RTL = "BOOKLET_RTL"
    
    #=================================
    # Signing mode Constants
    #=================================
    
    # Keystore type "pkcs12".
    KEYSTORE_TYPE_PKCS12 = "pkcs12";
    
    # Keystore type "jks".
    KEYSTORE_TYPE_JKS = "jks";
    
    # Signing mode for self-signed certificates.
    SIGNING_MODE_SELF_SIGNED = 1
    
    # Signing mode for VeriSign certificates.
    SIGNING_MODE_VERISIGN_SIGNED = 2
    
    # Signing mode for Windows certificates.
    SIGNING_MODE_WINCER_SIGNED = 3
    
    
    #=================================
    # JavaScript mode Constants
    #=================================
    
    # Indicates that JavaScript is disabled.
    # 
    # see setJavaScriptMode(int)
    JAVASCRIPT_MODE_DISABLED = 0;
    
    # Indicates that JavaScript is enabled.
    # 
    # see setJavaScriptMode(int)
    JAVASCRIPT_MODE_ENABLED = 1;
    
    # Indicates that JavaScript is enabled, without access to layout data.
    # 
    # see setJavaScriptMode(int)
    JAVASCRIPT_MODE_ENABLED_NO_LAYOUT = 2;
    
    # Indicates that JavaScript is enabled, without converter-specific 
    # optimizations to timeouts and intervals. This mode is significantly more 
    # time consuming and should only be used when no other mode provides the
    # expected results.
    # 
    # see setJavaScriptMode(int)
    JAVASCRIPT_MODE_ENABLED_REAL_TIME = 3;
    
    # Indicates that JavaScript is enabled, with time stamps increasing more quickly.
    # This makes some kinds of JS based animations (e.g. when using jQuery)
    # finish immediately, which has the same effect as JAVASCRIPT_MODE_ENABLED_REAL_TIME,
    # but is significantly faster. Only Date.getTime() is affected by this.
    # 
    # see setJavaScriptMode(int)
    JAVASCRIPT_MODE_ENABLED_TIME_LAPSE = 4;
    
    # The default JavaScript mode. It is set to 'JAVASCRIPT_MODE_DISABLED'
    # 
    # see setJavaScriptMode(int)
    JAVASCRIPT_MODE_DEFAULT = JAVASCRIPT_MODE_DISABLED;
    
    
    #=================================
    # HTTPS mode Constants
    #=================================
    
    # Indicates strict HTTPS behavior. This matches the default behavior of Java.
    # 
    # see setHttpsMode(int)
    HTTPS_MODE_STRICT = 0
    
    # Indicates lenient HTTPS behavior. This means that many certificate issues are ignored.
    # 
    # see setHttpsMode(int)
    HTTPS_MODE_LENIENT = 1
    
    # The default HTTPS mode. It is set to 'HTTPS_MODE_STRICT'.
    #
    # see setHttpsMode(int)
    HTTPS_MODE_DEFAULT = HTTPS_MODE_STRICT
    
    #=================================
    # Output Format Constants
    #=================================
    
    # PDF output format
    # 
    # see setOutputFormat(int, int, int)
    OUTPUT_FORMAT_PDF = 0
    
    # JPEG output format
    # 
    # see setOutputFormat(int, int, int)
    OUTPUT_FORMAT_JPEG = 1
    
    # PNG output format
    # 
    # see setOutputFormat(int, int, int)
    OUTPUT_FORMAT_PNG = 2
    
    # Transparent PNG output format
    # 
    # see setOutputFormat(int, int, int)
    OUTPUT_FORMAT_PNG_TRANSPARENT = 3
    
    # BMP output format
    # 
    # see setOutputFormat(int, int, int)
    OUTPUT_FORMAT_BMP = 4
    
    # GIF output format
    # 
    # see setOutputFormat(int, int, int)
    OUTPUT_FORMAT_GIF = 5
    
    # PNG output format (using Apache Imaging)
    # 
    # see setOutputFormat(int, int, int)
    OUTPUT_FORMAT_PNG_AI = 6
    
    # Transparent PNG output format (using Apache Imaging)
    # 
    # see setOutputFormat(int, int, int)
    OUTPUT_FORMAT_PNG_TRANSPARENT_AI = 7
    
    # LZW compressed TIFF output format
    # 
    # see setOutputFormat(int, int, int)
    OUTPUT_FORMAT_TIFF_LZW = 8
    
    # PackBits compressed TIFF output format
    # 
    # see setOutputFormat(int, int, int)
    OUTPUT_FORMAT_TIFF_PACKBITS = 9
    
    # Uncompressed TIFF output format
    # 
    # see setOutputFormat(int, int, int)
    OUTPUT_FORMAT_TIFF_UNCOMPRESSED = 10
    
    # Monochrome CCITT 1D compressed TIFF output format
    # 
    # see setOutputFormat(int, int, int)
    OUTPUT_FORMAT_TIFF_CCITT_1D = 11
    
    # Monochrome CCITT Group 3 compressed TIFF output format
    # 
    # see setOutputFormat(int, int, int)
    OUTPUT_FORMAT_TIFF_CCITT_GROUP_3 = 12
    
    # Monochrome CCITT Group 4 compressed TIFF output format
    # 
    # see setOutputFormat(int, int, int)
    OUTPUT_FORMAT_TIFF_CCITT_GROUP_4 = 13
     
    
    def __init__(self,host='localhost',port=9423,debug = False):
        """Constructor"""
        self.client = ROClient(host, port, "/pdfreactor/services/PDFreactor", debug)
        #Initialize Configuration Object
        self.PDFreactorConfiguration = confObj()
    
    #===================
    # System properties
    #===================
    
    def setLicenseKey(self,content):
        """Sets the license key using a string.
        
        The default value is None.
        
        param string content The content of the license key as a string.
        
        see setCacheFonts(boolean)
        see setFontCachePath(string)
        see addFontDirectory(string)"""
        self.PDFreactorConfiguration.in1["licenseKey"] = content
        
    def setDisableFontRegistration(self,value):
        """Enables or disables the font registration.
        
        If font registration is enabled and a valid font cache exists, then this font cache will be
        used. If font registration is disabled, any existing font cache will be ignored and the font
        directories will be scanned for font information.
        
        The default value is False.
        
        param boolean value The new value of the font registration setting.
        
        see setCacheFonts(boolean)
        see setFontCachePath(string)
        see addFontDirectory(string)"""
        self.PDFreactorConfiguration.in1["disableFontRegistration"] = value
        
    def addFont(self, source, family, bold, italic):
        """Loads a font from a URL which can be used via the CSS property "font-family".
        
        param source The URL to load the font from.
        param family The font family name the loaded font will be labeled as.
        param bold Whether the font will be labeled bold.
        param italic Whether the font will be labeled italic."""
        fontArray = {"source":source,"family":family,"bold":bold,"italic":italic}
        if (self.PDFreactorConfiguration.in1["fonts"] == None):
            self.PDFreactorConfiguration.in1["fonts"] = []
        self.PDFreactorConfiguration.in1["fonts"].append(fontArray)
        
    def addFontAlias(self, source, family, bold, italic):
        """Registers an alias font family for an existing font.
        
        This function is limited to fonts loaded automatically from system folders.
        
        param source The name of an existing font family.
        param family The alias name for that font.
        param bold Whether the alias will be labeled bold.
        param italic Whether the alias will be labeled italic."""
        fontArray = {"source":source,"family":family,"bold":bold,"italic":italic}
        if (self.PDFreactorConfiguration.in1["fontAliases"] == None):
            self.PDFreactorConfiguration.in1["fontAliases"] = []
        self.PDFreactorConfiguration.in1["fontAliases"].append(fontArray)
        
    def setCacheFonts(self, value):
        """Enables or disables caching of font information.
     
        During the PDF creation PDFreactor requires information about 
        fonts in the system. The process to get this information takes a 
        long time, thus PDFreactor offers an option to cache the collected 
        information about fonts.
        
        A font cache can be reused by PDFreactor on every PDF creation 
        process but only if font registration is enabled. If font registration 
        is disabled then the font cache will be ignored. (see
        setDisableFontRegistration(boolean) for more information).
        
        The default value is True. 
        
        param boolean value The new value of the cache fonts setting.
        
        see setDisableFontRegistration(boolean)
        see setFontCachePath(string)
        see addFontDirectory(string)"""    
        self.PDFreactorConfiguration.in1["cacheFonts"] = value
    
    def setFontCachePath(self,location):
        """Sets the path of the font cache.
    
        This path will be used to read and write the font cache. If the font cache path is set to
        None then the "user.home" directory will be used. 
        
        The default value is None.
        
        param string location The path of the font cache.
        
        see setDisableFontRegistration(boolean)
        see setCacheFonts(boolean)
        see addFontDirectory(string)"""
        self.PDFreactorConfiguration.in1["fontCachePath"] = location
      
    def setFontDirectory(self,location):
        """deprecated. As of PDFreactor 6.0, replaced by addFontDirectory(String)
        
        see addFontDirectory(String)"""
        self.PDFreactorConfiguration.in1["fontDirectory"] = location
    
    def addFontDirectory(self,fontDirectory):
        """Registers an additional font directory to load fonts from.
        
        param fontDirectory The path of the font directory."""
        if (self.PDFreactorConfiguration.in1["fontDirectories"] == None):
            self.PDFreactorConfiguration.in1["fontDirectories"] = []
        self.PDFreactorConfiguration.in1["fontDirectories"].append(fontDirectory)
      
    def setLogLevel(self,value):
        """Sets the log level. 
    
        Use one of the 'LOG_LEVEL_' constants to specify the log
        
        param int value The new log level setting.
        
        see LOG_LEVEL_NONE
        see LOG_LEVEL_FATAL
        see LOG_LEVEL_WARN
        see LOG_LEVEL_INFO
        see LOG_LEVEL_DEBUG
        see LOG_LEVEL_PERFORMANCE
        see LOG_LEVEL_DEFAULT
        see getLog()"""
        self.PDFreactorConfiguration.in1["logLevel"] = value
        
    def setLogExceedingContent(self, logExceedingContentAnalyze, logExceedingContentAgainst):
        """Whether to log content exceeding the page.
        
        Use 'EXCEEDING_CONTENT_ANALYZE_' constants to specify
        which kind of content should be observed for exceeding content logging.
        
        The default value is 'EXCEEDING_CONTENT_ANALYZE_NONE'.
        
        param int logExceedingContentAnalyze Enables logging of exceeding content and optionally of boxes.
        param int logExceedingContentAgainst Enables logging of exceeding content either against the page edges, page content areas or containers.
        
        see EXCEEDING_CONTENT_ANALYZE_NONE
        see EXCEEDING_CONTENT_ANALYZE_CONTENT
        see EXCEEDING_CONTENT_ANALYZE_CONTENT_AND_BOXES
        see EXCEEDING_CONTENT_ANALYZE_CONTENT_AND_STATIC_BOXES
        see EXCEEDING_CONTENT_AGAINST_NONE
        see EXCEEDING_CONTENT_AGAINST_PARENT
        see EXCEEDING_CONTENT_AGAINST_PAGE_CONTENT
        see EXCEEDING_CONTENT_AGAINST_PAGE_BORDERS"""
        self.PDFreactorConfiguration.in1["logExceedingContentAnalyze"] = logExceedingContentAnalyze
        self.PDFreactorConfiguration.in1["logExceedingContentAgainst"] = logExceedingContentAgainst
    
    def setThrowLicenseExceptions(self,value):
        """Whether an exception should be thrown when no legal full license key is set. 
        This allows to programmatically ensure that documents are not altered due to license issues.
        
        The default value is False."""
        self.PDFreactorConfiguration.in1["throwLicenseExceptions"] = value
    
    #=========================
    # XML document properties
    #=========================
    
    def setBaseURL(self,value):
        """Sets the base URL of the XML document. 
    
        To resolve relative URLs to absolute URLs a reference (base) URL is required. This
        reference URL is usually the system id of the document. This method can be used to
        specify another reference URL. If this URL is not None then it will be used
        instead of the system id.
        
        The default value is None.
        
        param string value The base URL for the document."""
        self.PDFreactorConfiguration.in1["baseURL"] = value
      
    def setXSLTMode(self,value):
        """Enables or disables XSLT transformations.
     
        Set this value to True to enable XSLT transformations or to False to disable
        XSLT transformations. 
        
        The default value is False.
        
        param boolean value The new XSLT mode."""
        self.PDFreactorConfiguration.in1["XSLTMode"] = value
    
    def setJavaScriptMode(self,javaScriptMode):
        """Sets the JavaScript Mode.
        
        The default value is 'JAVASCRIPT_MODE_DISABLED'.
        
        param int javaScriptMode The JavaScript mode.
        
        see JAVASCRIPT_MODE_DISABLED
        see JAVASCRIPT_MODE_ENABLED
        see JAVASCRIPT_MODE_ENABLED_NO_LAYOUT
        see JAVASCRIPT_MODE_ENABLED_REAL_TIME
        see JAVASCRIPT_MODE_ENABLED_TIME_LAPSE"""
        self.PDFreactorConfiguration.in1["javaScriptMode"] = javaScriptMode
        
    def setHTTPSMode(self, httpsMode):
        """Sets the HTTPS Mode.
        
        In closed environment lenient can be the preferred setting to avoid HTTPS issues that are not security critical.
        
        The default value is 'HTTPS_MODE_STRICT'.
        
        param int httpsMode The HTTPS mode.
        
        see HTTPS_MODE_STRICT
        see HTTPS_MODE_LENIENT"""
        self.PDFreactorConfiguration.in1["httpsMode"] = httpsMode
        
    def setEncoding(self,value):
        """Sets the encoding of the document.
    
        If this value is set to None or it is empty then the encoding will be detected
        automatically. 
        
        The default value is None.
        
        param string value The encoding of the document or None for autodetection."""
        self.PDFreactorConfiguration.in1["encoding"] = value
    
    def setCleanupTool(self,value):
        
        """Sets the cleanup tool to use for documents with unparsable content.
        
        The 'CLEANUP_' constants can be used as value. The 
        default value specified is 'CLEANUP_CYBERNEKO'.
        
        HTML5 utilizes an internal cleanup.
        
        param int value The new cleanup tool.
        
        see CLEANUP_NONE
        see CLEANUP_JTIDY
        see CLEANUP_CYBERNEKO
        see CLEANUP_TAGSOUP"""
        self.PDFreactorConfiguration.in1["cleanupTool"] = value
    
    def setDocumentType(self,value):
        """Sets the document type. 
    
        The 'DOCTYPE_' constants can be used to specify the 
        document type. The default value specified is 'DOCTYPE_AUTODETECT'.
        
        The default value specified by DOCTYPE_DEFAULT is DOCTYPE_AUTODETECT.
        
        param int value The new document type setting.
        
        see DOCTYPE_AUTODETECT
        see DOCTYPE_XML
        see DOCTYPE_XHTML
        see DOCTYPE_HTML5"""
        self.PDFreactorConfiguration.in1["documentType"] = value
        
    def setPostTransformationDocumentType(self,value):
        """Sets the document type after XSL-Transformations have been applied.
        
        The 'DOCTYPE_' constants can be used to specify the 
        document type. The default value specified is 'DOCTYPE_AUTODETECT'.
        
        param int value The new document type setting.
        
        see DOCTYPE_AUTODETECT
        see DOCTYPE_XML
        see DOCTYPE_XHTML
        see DOCTYPE_HTML5"""
        self.PDFreactorConfiguration.in1["postTransformationDocumentType"] = value
    
    def addUserStyleSheet(self, content, media, title, URI):
        """Adds a user style sheet to the document. 
    
        There are two ways to specify the style sheet:
        
        - Specifying the style sheet only using an URI.
        - Specifying the style sheet by the content of the stylesheet and alternatively setting a URI to
          resolve relative elements. If no URI is specified then the system id/base URL of the document will be
          used.
        
        param string content The content of the style sheet.
        param string media The media type of the style sheet.
        param string title The title of the stylesheet.
        param string uri The URI of the style sheet.
        
        see addUserStyleSheet(InputSource)
        see removeAllUserStyleSheets()"""
        if self.PDFreactorConfiguration.in1["userStyleSheets"] == None:
            self.PDFreactorConfiguration.in1["userStyleSheets"] = []
            stylesArray = {'content':content, 'media':media, 'title':title, 'URI':URI}
            self.PDFreactorConfiguration.in1["userStyleSheets"].append(stylesArray)
        else:
            stylesArray = {'content':content, 'media':media, 'title':title, 'URI':URI}
            self.PDFreactorConfiguration.in1["userStyleSheets"].append(stylesArray)
    
    def removeAllUserStyleSheets(self):
        """Removes all user style sheets.
    
        see addUserStyleSheet(string,string,string,string)
        see addUserStyleSheet(InputSource)"""
        self.PDFreactorConfiguration.in1["userStyleSheets"] = None
    
    def addXSLTStyleSheet(self, content, URI):
        """Adds a XSLT style sheet to the document. 
    
        There are two ways to specify the style sheet:
        
        - Specifying the style sheet only using an URI.
        - Specifying the style sheet by the content of the stylesheet and alternatively setting a URI to
          resolve relative elements. If no URI is specified then the system id/base URL of the document will be
          used.
        
        param string content The content of the style sheet.
        param string URI The URI of the style sheet.
        
        see removeAllXSLTStyleSheets()"""
        if self.PDFreactorConfiguration.in1["XSLTStyleSheets"] == None:
            self.PDFreactorConfiguration.in1["XSLTStyleSheets"] = []
            stylesArray = {'content':content, 'URI':URI}
            self.PDFreactorConfiguration.in1["XSLTStyleSheets"].append(stylesArray)
        else:
            stylesArray = {'content':content, 'URI':URI}
            self.PDFreactorConfiguration.in1["XSLTStyleSheets"].append(stylesArray)
    
    def removeAllXSLTStyleSheets(self):
        """Removes all user style sheets.
    
        see addXSLTStyleSheet(string, string)"""
        self.PDFreactorConfiguration.in1["XSLTStyleSheets"] = None
    
    def addUserScript(self, content, URI, beforeDocumentScripts):
        """Adds an user script to the document.
        
        There are two ways to specify the script:
        
        - Specifying the script only by an URI.
        - Specifying the script by the content of the script and
        alternatively setting a URI to resolve relative elements. If no URI
        is specified then the system id/base URL of the document will be used.
        
        param string content The content of the script.
        param string URI The URI of the script.
        param boolean beforeDocumentScripts Use True to cause PDFreactor to run the script before all scripts inside the document and False to run it after.
        
        see removeAllUserScripts()"""
        scriptsArray = {'content':content, 'URI':URI, 'beforeDocumentScripts':beforeDocumentScripts}
        if (self.PDFreactorConfiguration.in1["userScripts"] == None):
            self.PDFreactorConfiguration.in1["userScripts"] = []
        self.PDFreactorConfiguration.in1["userScripts"].append(scriptsArray)
    
    def removeAllUserScripts(self):
        """Removes all user scripts.
        
        see addUserScript(string, string, boolean)"""
        self.PDFreactorConfiguration.in1["UserScripts"] = None
    
    #=========================
    # PDF document properties
    #=========================
    
    def setAuthor(self,value):
        """Sets the value of the author field of the PDF document.
    
        param string value The author of the document."""
        self.PDFreactorConfiguration.in1["author"] = value
      
    def setCreator(self,value):
        """Sets the value of creator field of the PDF document.
    
        param string value The creator of the document."""
        self.PDFreactorConfiguration.in1["creator"] = value
      
    def setKeywords(self,value):
        """Sets the value of the keywords field of the PDF document.
    
        param string value The keywords of the document."""
        self.PDFreactorConfiguration.in1["keywords"] = value
        
    def setTitle(self,value):
        """Sets the value of the title field of the PDF document.
    
        param string value The title of the document."""
        self.PDFreactorConfiguration.in1["title"] = value
      
    def setSubject(self,value):
        """Sets the value of the subject field of the PDF document.
    
        param string value The subject of the document.""" 
        self.PDFreactorConfiguration.in1["subject"] = value
        
    def addCustomDocumentProperty(self,name,value):
        """Adds a custom property to the PDF document. An existing 
        property of the same name will be replaced.
        
        param string name The name of the property.
        param string value The value of the property."""
        self.PDFreactorConfiguration.in1["customDocumentProperties"].append([name, value])
        
    def addAttachment(self,data,url,name,description):
        """Adds a file attachment to PDF document.
        
        param string data The base64encoded binary content of the attachment. May be None.
        param string url If data is None, the attachment will be retrieved from this URL. 
                If this is "#" the input document URL is used instead.
        param string name The file name associated with the attachment. It is recommended to specify
                the correct file extension. If this is None the name is derived from the URL.
        param string description The description of the attachment. If this is None the name is used."""
        if self.PDFreactorConfiguration.in1["attachments"] == None:
            self.PDFreactorConfiguration.in1["attachments"] = []
            
        stylesArray = {'data':data, 'url':url, 'name':name, 'description':description}
        
        self.PDFreactorConfiguration.in1["attachments"].append(stylesArray)
    def setDocumentDefaultLanguage(self,languageCode):
        """Sets the language used for documents having no explicit language attribute set.
        
        The language code is used to resolve the lang() selector correct and
        to determine the correct language used for hyphenation.
        
        param string languageCode the default ISO 639 language code used for documents.""" 
        self.PDFreactorConfiguration.in1["documentDefaultLanguage"] = languageCode
        
    def setEncryption(self,value):
        """Sets the encryption.
    
        Use one of the following ENCRYPTION_ constants to specify the encryption:<br>
        
        The default value specified is ENCRYPTION_NONE.
        
        param int value The new encryption setting.
        
        see #ENCRYPTION_NONE
        see #ENCRYPTION_40
        see #ENCRYPTION_128
        see setOwnerPassword(string)
        see setUserPassword(string)
        see setAllowAnnotations(boolean)
        see setAllowAssembly(boolean)
        see setAllowCopy(boolean)
        see setAllowDegradedPrinting(boolean)
        see setAllowFillIn(boolean)
        see setAllowModifyContents(boolean)
        see setAllowPrinting(boolean)
        see setAllowScreenReaders(boolean)"""
        self.PDFreactorConfiguration.in1["encryption"] = value
        
    def setFullCompression(self,value):
        """Enables or disables full compression of the PDF document. 
    
        The default value is False.
        
        param boolean value True to enable full compression of the document and
        False to disable full compression."""
        self.PDFreactorConfiguration.in1["fullCompression"] = value
        
    def setOwnerPassword(self,value):
        """Sets the owner password of the PDF document.
    
        The default value is None
        
        param string value The owner password.
        
        see setEncryption(int)
        see setUserPassword(string)"""
        self.PDFreactorConfiguration.in1["ownerPassword"] = value
        
    def setUserPassword(self,value):
        """Sets the user password of the PDF document.
    
        The default value is None.
        
        param string value The user password.
        
        see setEncryption(int)
        see setOwnerPassword(string)"""
        self.PDFreactorConfiguration.in1["userPassword"] = value
        
    def setAuthenticationCredentials(self, username, password):
        """Enables access to resources that are secured via Basic or Digest authentication.

        param string username The user name for the secured realm.
        param string password The password for the secured realm."""
        self.PDFreactorConfiguration.in1["authenticationUsername"] = username
        self.PDFreactorConfiguration.in1["authenticationPassword"] = password

    def setRequestHeader(self, key, value):
        """"Adds a request header to all outgoing HTTP connections. If the key already exists, the pair is overwritten.
        
        param string key The key of the header.
        param string value The value of the header."""
        self.PDFreactorConfiguration.in1["requestHeaderMap"].append([key, value])

    def setCookie(self, key, value):
        """Adds a cookie to all outgoing HTTP connections. If the key already exists, the pair is overwritten.

        param string key The key of the cookie.
        param string value The value of the cookie."""
        self.PDFreactorConfiguration.in1["cookies"].append([key, value])
        
    def setAddLinks(self,value):
        """Enables or disables links in the PDF document.
    
        The default value is False.
        
        param boolean value Use True to enable links in the document and False to
        disable links."""
        self.PDFreactorConfiguration.in1["addLinks"] = value
        
    def setAddBookmarks(self,value):
        """Enables or disables bookmarks in the PDF document.
    
        The default value is False.
        
        param boolean value Use True to enable bookmarks in the document and False
        to disable bookmarks."""
        self.PDFreactorConfiguration.in1["addBookmarks"] = value
        
    def setAddTags(self,value):
        """Enables or disables tagging of PDF document.
    
        The default value is False.
        
        param boolean value Use True to enable tagging of the document and
        False to disable tagging."""
        self.PDFreactorConfiguration.in1["addTags"] = value
        
    def setAddPreviewImages(self,value):
        """Enables or disables embedding of image previews per page in the PDF document.
    
        The default value is False.
        
        param boolean value Use True to enable embedding of image previews per page in
        the document and False to disable embedding of image previews per page."""
        self.PDFreactorConfiguration.in1["addPreviewImages"] = value
        
    def setAddAttachments(self,value):
        """Enables or disables attachments specified in style sheets.
        
        The default value is False.
        
        param boolean value Whether to enable CSS based attachments."""
        self.PDFreactorConfiguration.in1["addAttachments"] = value
        
    def setAddOverprint(self,value):
        """Enables or disables overprinting.
        
        The default value is False.
        
        param boolean value Whether to enable overprinting."""
        self.PDFreactorConfiguration.in1["addOverprint"] = value
        
    def setAddPrintDialogPrompt(self,value):
        """Enables or disables a print dialog to be shown upon opening the generated PDF document by a
        PDF viewer.
        
        The default value is False.
        
        param boolean value Use True to enable a print dialog to be shown upon document
        opening by a PDF viewer and False to disable the print dialog prompt."""
        self.PDFreactorConfiguration.in1["addPrintDialogPromt"] = value
        
    def setAppendLog(self,value):
        """Specifies whether or not the log data should be added to the
        PDF document.
        
        The default value is False.
        
        param boolean value Use True to add the log data to the document and
        False if the log data should not be added."""
        self.PDFreactorConfiguration.in1["appendLog"] = value
        
    def setAllowAnnotations(self,value):
        """Enables or disables the 'annotations' restriction in the PDF document.
    
        The default value is False.
        
        param boolean value Use True to enable 'annotations' in the document and
        False to disable 'annotations'.
        
        see setEncryption(int)"""
        self.PDFreactorConfiguration.in1["allowAnnotations"] = value
        
    def setAllowAssembly(self,value):
        """Enables or disables the 'assembly' restriction in the PDF document.
    
        The default value is False.
        
        param boolean value Use True to enable 'assembly' in the document and
        False to disable 'assembly'.
        
        see setEncryption(int)"""
        self.PDFreactorConfiguration.in1["allowAssembly"] = value
        
    def setAllowCopy(self,value):
        """Enables or disables the 'copy' restriction in the PDF document.
    
        The default value is False.
        
        param boolean value Use True to enable 'copy' in the document and
        False to disable 'copy'.
        
        see setEncryption(int)"""
        self.PDFreactorConfiguration.in1["allowCopy"] = value
        
    def setAllowDegradedPrinting(self,value):
        """Enables or disables the 'degraded printing' restriction in the PDF
        document.
        
        The default value is False.
        
        param boolean value Use True to enable 'degraded printing' in the document and
        False to disable 'degraded printing'.
        
        see setEncryption(int)"""
        self.PDFreactorConfiguration.in1["allowDegradedPrinting"] = value
        
    def setAllowFillIn(self,value):
        """Enables or disables the 'fill in' restriction in the PDF document.
    
        The default value is False.
        
        param boolean value Use True to enable 'fill in' in the document and
        False to disable 'fill in'.
        
        see setEncryption(int)"""
        self.PDFreactorConfiguration.in1["allowFillIn"] = value
        
    def setAllowModifyContents(self,value):
        """Enables or disables the 'modify contents' restriction in the PDF
        document.
        
        The default value is False.
        
        param boolean value Use True to enable 'modify contents' in the document and
        False to disable 'modify contents'.
        
        see setEncryption(int)"""
        self.PDFreactorConfiguration.in1["allowModifyContents"] = value
        
    def setAllowPrinting(self,value):
        """Enables or disables the 'printing' restriction in the PDF document.
    
        The default value is False.
        
        param boolean value Use True to enable 'printing' in the document and
        False to disable 'printing'.
        
        see setEncryption(int)"""
        self.PDFreactorConfiguration.in1["allowPrinting"] = value
        
    def setAllowScreenReaders(self,value):
        """Enables or disables the 'screen readers' restriction in the PDF
        document.
        
        The default value is False.
        
        param boolean value Use True to enable 'screen readers' in the document and
        False to disable 'screen readers'.
        
        see setEncryption(int)"""
        self.PDFreactorConfiguration.in1["allowScreenReaders"] = value
        
    def setDisableFontEmbedding(self,value):
        """Sets whether fonts will not be embedded into the resulting PDF. 
        Setting this to True will reduce the file size of the output document.
        However, the resulting PDF documents are no longer guaranteed to look 
        identical on all systems.
        
        The default value is False."""
        self.PDFreactorConfiguration.in1["disableFontEmbedding"] = value
        
    def setFontFallback(self,value):
        """Sets a list of fallback font families used for character substitution. This 
        list is iterated for characters that can not be displayed with any of the fonts 
        specified via the CSS property font-family.
        
        param string[] fontFallback an array of font family names"""
        self.PDFreactorConfiguration.in1["fontFallback"] = value
        
    def setPixelsPerInch(self,value):
        """Sets the pixels per inch. 
        Changing this value changes the physical length of sizes specified in px (including those 
        specified via HTML attributes).
        
        The default value is 96ppi."""
        self.PDFreactorConfiguration.in1["pixelsPerInch"] = value
        
    def setPixelsPerInchShrinkToFit(self,value):
        """Whether the pixels per inch should be adapted automatically to avoid content exceeding pages."""
        self.PDFreactorConfiguration.in1["pixelsPerInchShrinkToFit"] = value
        
    def setPageOrder(self,value):
        """Sets the page order of the direct result of the conversion.
        
        param string order A comma-separated list of page numbers and ranges is 
                           intended as parameter. Alternatively, 'PAGE_ORDER_'
                           constants can be used.
        
        see #PAGE_ORDER_EVEN
        see #PAGE_ORDER_ODD 
        see #PAGE_ORDER_BOOKLET
        see #PAGE_ORDER_BOOKLET_RTL"""
        self.PDFreactorConfiguration.in1["pageOrder"] = value
        
    def setPagesPerSheetProperties(self, cols, rows, sheetSize, sheetMargin, spacing, direction):
        """Sets the properties of a sheet on which multiple pages are being arranged.
        
        If 'cols' or 'rows' is less than 1, no 
        pages-per-sheet processing is done. This is the case by default.
        
        Use one of the 'PAGES_PER_SHEET_DIRECTION_' constants to 
        specify the the direction. The default value is 'PAGES_PER_SHEET_DIRECTION_RIGHT_DOWN'

        param int cols The number of columns per sheet.
        param int rows The number of rows per sheet.
        param string sheetSize The sheet size as CSS size, e.g. 'A4', 'letter landscape', '15in 20in',
                               '20cm 30cm'.
        param string sheetMargin The sheet margin as CSS margin, e.g. '1in', '1cm 1.5cm', '10mm 20mm 10mm 30mm'. 'None' is 
                                 interpreted as '0mm'.
        param string spacing The horizontal and vertical space between pages on a sheet as CSS value, e.g. '0.1in', '5mm 2mm'. 'None' is 
                             interpreted as '0mm'.
        param int direction The direction in which the pages are ordered on a sheet.
        
        see #PAGES_PER_SHEET_DIRECTION_DOWN_LEFT
        see #PAGES_PER_SHEET_DIRECTION_DOWN_RIGHT
        see #PAGES_PER_SHEET_DIRECTION_LEFT_DOWN
        see #PAGES_PER_SHEET_DIRECTION_LEFT_UP
        see #PAGES_PER_SHEET_DIRECTION_RIGHT_DOWN
        see #PAGES_PER_SHEET_DIRECTION_RIGHT_UP
        see #PAGES_PER_SHEET_DIRECTION_UP_LEFT
        see #PAGES_PER_SHEET_DIRECTION_UP_RIGHT"""
        self.PDFreactorConfiguration.in1["pagesPerSheetCols"] = cols
        self.PDFreactorConfiguration.in1["pagesPerSheetRows"] = rows
        self.PDFreactorConfiguration.in1["pagesPerSheetSheetSize"] = sheetSize
        self.PDFreactorConfiguration.in1["pagesPerSheetSheetMargin"] = sheetMargin
        self.PDFreactorConfiguration.in1["pagesPerSheetSpacing"] = spacing
        self.PDFreactorConfiguration.in1["pagesPerSheetDirection"] = direction
        
    def setBookletMode(self, sheetSize, sheetMargin, rtl):
        """Convenience method to set pages-per-sheet properties and page order in one step to create a booklet.
        
        param string sheetSize The size of the sheet as CSS value, e.g. 'A3', 'letter landscape', '15in 20in',
                               '20cm 30cm'.
        param string sheetMargin The sheet margin as CSS margin, e.g. '1in', '1cm 1.5cm', '10mm 20mm 10mm 30mm'. 'None' is 
                                 interpreted as '0mm'.
        param boolean rtl Whether or not the reading order of the booklet should be right-to-left."""
        self.PDFreactorConfiguration.in1["bookletSheetSize"] = sheetSize
        self.PDFreactorConfiguration.in1["bookletSheetMargin"] = sheetMargin
        self.PDFreactorConfiguration.in1["bookletRTL"] = rtl
        self.PDFreactorConfiguration.in1["bookletModeEnabled"] = value
        
    #=====================
    # Merge methods
    #=====================
        
    def setMergeURL(self,value):
        """This methods sets a URL of an external PDF document which will be merged with the PDF
        document generated by the XML source.
        
        The default value is None
        
        param string url A URL of a PDF document.
        
        see setMergeByteArray(byte[])
        see setMergeBeforePDF(boolean)"""
        self.PDFreactorConfiguration.in1["mergeURL"] = value
        
    def setMergeURLs(self,value):
        """This method sets an array of URLs of external PDF documents which will be
        merged with the PDF document generated by the XML source.
        
        param string[] urls An array of URLs of PDF documents."""
        self.PDFreactorConfiguration.in1["mergeURLs"] = value
        
    def setMergeByteArray(self,value):
        """This methods sets a byte array containing an external PDF document which will be merged with
        the PDF document generated by the XML source.
        
        The default value is None
        
        param string base64string A base64encoded binary string containing the PDF RAW data.
        
        see setMergeURL(string)
        see setMergeURLs(string[])
        see setMergeByteArrays(byte[][])
        see setMergeMode(int)"""
        self.PDFreactorConfiguration.in1["mergeByteArray"] = value
        
    def setMergeByteArrays(self,value):
        """This method sets an array of several byte arrays containing external PDF 
        documents which will be merged with the PDF document generated by the XML source.
        
        param byte[] base64strings An array of byte arrays containing multiple PDF RAW data.
        
        see setMergeByteArray(byte[])
        see setMergeURL(string)
        see setMergeURLs(string[])
        see setMergeMode(int)"""
        self.PDFreactorConfiguration.in1["mergeByteArrays"] = value
        
    def setMergeBeforePDF(self,value):
        """deprecated. As of PDFreactor 5.0, replaced by setMergeMode(int)
        
        see setMergeMode(int)"""
        if value == True:
            self.setMergeMode(self.MERGE_MODE_PREPEND)
        else:
            self.setMergeMode(self.MERGE_MODE_APPEND)
        
    def setMergeMode(self,value):
        """Sets the merge mode.
        
        The following merge methods can be used:
        
        - append (MERGE_MODE_APPEND)
        - prepend (MERGE_MODE_PREPEND)
        - overlay above the content of the generated PDF (MERGE_MODE_OVERLAY)
        - overlay below the content of the generated PDF (MERGE_MODE_OVERLAY_BELOW)
        
        The default value is MERGE_MODE_APPEND.
        
        see MERGE_MODE_APPEND
        see MERGE_MODE_PREPEND
        see MERGE_MODE_OVERLAY
        see MERGE_MODE_OVERLAY_BELOW"""
        self.PDFreactorConfiguration.in1["mergeMode"] = value
        
    def setOverlayRepeat(self, value):
        """If one of the documents of an overlay process is shorter than the other, this method 
        allows repeating either its last page or all of its pages in order to overlay all pages of 
        the longer document.
        
        Use one of the 'OBERLAY_REPEAT_' constants to specify the 
        overlay repeat. The default value is 'OVERLAY_REPEAT_NONE'.
        
        see OVERLAY_REPEAT_NONE
        see OVERLAY_REPEAT_LAST_PAGE
        see OVERLAY_REPEAT_ALL_PAGES
        
        The default value is OVERLAY_REPEAT_NONE."""
        self.PDFreactorConfiguration.in1["overlayRepeat"] = value
    
    #==================
    # Digitally signing
    #==================
    
    def setSignPDF(self, keystoreURL, keyAlias, keystorePassword, keystoreType, signingMode):
        """Sets a digital certificate to sign the newly created PDF.</p>
        
        Requires a keystore file. The included certificate may be self-signed.</p>
        
        Use the 'KEYSTORE_TYPE_' constants to specify the keystore type.
        
        Use the 'SIGNING_MODE_' constants to specify the signing mode.
        
        param string keystoreURL The URL to the keystore file.
        param string keyAlias The alias of the certificate included in the keystore to be used to sign the PDF.
        param string keystorePassword The password of the keystore.
        param string keystoreType The format of the keystore, i.e. 'pkcs12' or 'jks'. 
        Use one of the 'KEYSTORE_TYPE_' constants as value.
        param int signingMode The mode that is used to sign the PDF, i.e. 'self-signed', 
        'Windows certificate' or 'VeriSign'.
        Use one of the 'SIGNING_MODE_' constants as value.
        
        see KEYSTORE_TYPE_JKS
        see KEYSTORE_TYPE_PKCS12
        see SIGNING_MODE_SELF_SIGNED
        see SIGNING_MODE_VERISIGN_SIGNED
        see SIGNING_MODE_WINCER_SIGNED"""
        self.PDFreactorConfiguration.in1["signPdfKeystoreURL"] = keystoreURL
        self.PDFreactorConfiguration.in1["signPdfKeyAlias"] = keyAlias
        self.PDFreactorConfiguration.in1["signPdfKeystorePassword"] = keystorePassword
        self.PDFreactorConfiguration.in1["signPdfKeystoreType"] = keystoreType
        self.PDFreactorConfiguration.in1["signPdfSigningMode"] = signingMode

    #===================
    # Viewer Prefernces
    #===================

    def setViewerPreferences(self,viewerPreferences):
        """Sets the page layout and page mode preferences of the PDF.
        
        Use the 'VIEWER_PREFERENCES_' constants to specify the 
        viewer preferences. By default no viewer preference is set.
        
        param int viewerPreferences ORed VIEWERPREFERENCES_ constants.
        
        see #VIEWER_PREFERENCES_CENTER_WINDOW
        see #VIEWER_PREFERENCES_DIRECTION_L2R
        see #VIEWER_PREFERENCES_DIRECTION_R2L
        see #VIEWER_PREFERENCES_DISPLAY_DOC_TITLE
        see #VIEWER_PREFERENCES_DUPLEX_FLIP_LONG_EDGE
        see #VIEWER_PREFERENCES_DUPLEX_FLIP_SHORT_EDGE
        see #VIEWER_PREFERENCES_DUPLEX_SIMPLEX
        see #VIEWER_PREFERENCES_FIT_WINDOW
        see #VIEWER_PREFERENCES_HIDE_MENUBAR
        see #VIEWER_PREFERENCES_HIDE_TOOLBAR
        see #VIEWER_PREFERENCES_HIDE_WINDOW_UI
        see #VIEWER_PREFERENCES_NON_FULLSCREEN_PAGE_MODE_USE_NONE
        see #VIEWER_PREFERENCES_NON_FULLSCREEN_PAGE_MODE_USE_OC
        see #VIEWER_PREFERENCES_NON_FULLSCREEN_PAGE_MODE_USE_OUTLINES
        see #VIEWER_PREFERENCES_NON_FULLSCREEN_PAGE_MODE_USE_THUMBS
        see #VIEWER_PREFERENCES_PAGE_LAYOUT_ONE_COLUMN
        see #VIEWER_PREFERENCES_PAGE_LAYOUT_SINGLE_PAGE
        see #VIEWER_PREFERENCES_PAGE_LAYOUT_TWO_COLUMN_LEFT
        see #VIEWER_PREFERENCES_PAGE_LAYOUT_TWO_COLUMN_RIGHT
        see #VIEWER_PREFERENCES_PAGE_LAYOUT_TWO_PAGE_LEFT
        see #VIEWER_PREFERENCES_PAGE_LAYOUT_TWO_PAGE_RIGHT
        see #VIEWER_PREFERENCES_PAGE_MODE_FULLSCREEN
        see #VIEWER_PREFERENCES_PAGE_MODE_USE_NONE
        see #VIEWER_PREFERENCES_PAGE_MODE_USE_OC
        see #VIEWER_PREFERENCES_PAGE_MODE_USE_OUTLINES
        see #VIEWER_PREFERENCES_PAGE_MODE_USE_THUMBS
        see #VIEWER_PREFERENCES_PICKTRAYBYPDFSIZE_FALSE
        see #VIEWER_PREFERENCES_PICKTRAYBYPDFSIZE_TRUE
        see #VIEWER_PREFERENCES_PRINTSCALING_APPDEFAULT
        see #VIEWER_PREFERENCES_PRINTSCALING_NONE"""
        self.PDFreactorConfiguration.in1["viewerPreferences"] = viewerPreferences
    
    
    def setConformance(self, conformance):
        """Sets the conformance of the PDF.
        
        The 'CONFORMANCE_' constants can be used as value. The default 
        value specified is 'CONFORMANCE_PDF'.
        
        param int conformance conformance constants.
        
        see CONFORMANCE_PDF
        see CONFORMANCE_PDFA"""
        self.PDFreactorConfiguration.in1["conformance"] = conformance
    
    def setDefaultColorSpace(self, defaultColorSpace):
        """Sets whether to convert color key words to CMYK instead of RGB.
        
        The 'COLOR_SPACE_' constants can be used as value.
        The default value specified is 'COLOR_SPACE_RGB'.
        
        param boolean defaultColorSpace whether to prefer CMYK.
        
        see COLOR_SPACE_CMYK
        see COLOR_SPACE_RGB"""
        self.PDFreactorConfiguration.in1["defaultColorSpace"] = defaultColorSpace
    
    def setOutputIntentFromURL(self, identifier, profileUrl):
        """Sets the output intent including the identifier and the ICC profile to be embedded into the PDF.
        
        param string identifier the OutputConditionIdentifier.
        param string profileUrl the DestOutputProfile."""
        self.PDFreactorConfiguration.in1["outputIntentIdentifier"] = identifier
        self.PDFreactorConfiguration.in1["outputIntentICCProfileURL"] = profileUrl
        self.PDFreactorConfiguration.in1["outputIntentICCProfileData"] = None
    
    def setOutputIntentFromByteArray(self, identifier, profileData):
        """Sets the output intent including the identifier and the ICC profile to be embedded into the PDF.
        
        param string identifier the OutputConditionIdentifier.
        param string profileData the base64encoded binary content of the DestOutputProfile."""
        self.PDFreactorConfiguration.in1["outputIntentIdentifier"] = identifier
        self.PDFreactorConfiguration.in1["outputIntentICCProfileData"] = profileData
        self.PDFreactorConfiguration.in1["outputIntentICCProfileURL"] = None
    
    def setProcessingPreferences(self, processingPreferences):
        """Preferences that influence the conversion process without changing the output
        
        Use the 'PROCESSING_PREFERENCES_' constants to specify the processing preferences.
        By default no processing preference is set.
        
        param int processingPreferences ORed processing preferences flags.
        
        #see PROCESSING_PREFERENCES_SAVE_MEMORY_IMAGES"""
        self.PDFreactorConfiguration.in1["processingPreferences"] = processingPreferences
    
    #================
    # Render methods
    #================
    
    def setContinuousOutput(self,width,height):
        """Enables the conversion of the input document into one image. 
        
        param int width equivalent to the width of a browser window (view port). Values <1 enable paginated output
        param int height equivalent to the height of a browser window (view port). For values <1 the entire height of the document is used."""
        self.PDFreactorConfiguration.in1["continuousWidth"] = width
        self.PDFreactorConfiguration.in1["continuousHeight"] = height
    
    def renderDocumentFromURL(self,url):
        """Generates a PDF document from an XML document at a URL.
        
        The document can be specified by a URL pointing to the document.
        
        param string url A URL pointing to the XML document.
        return string The PDF document as a base64encoded binary string.
        
        see renderDocumentFromByteArray()
        see renderDocumentFromContent()"""
        in0=url
        in1=self.PDFreactorConfiguration.in1
        args = {"in0" : in0, "in1" : in1}
        
        self.resp = self.client.ROCall("renderDocumentFromURL", args)
        return self.resp["pdf"]
        
    def renderDocumentFromByteArray(self,byteArray):
        """Generates a PDF document from an XML document inside a byte array.
        
        The document can be specified by a byte array containing the content of the document.
        
        param string byteArray A base64encoded binary string containing the content of the XML
        document.
        
        return string The PDF document as a base64encoded binary string.
        
        see renderDocumentFromURL()
        see renderDocumentFromContent()
        see renderDocumentFromByteArrayAsArray()"""
        in0=byteArray
        in1=self.PDFreactorConfiguration.in1
        args = {"in0" : in0, "in1" : in1}
        
        self.resp = self.client.ROCall("renderDocumentFromByteArray",args)
        return self.resp["pdf"]
        
    def renderDocumentFromContent(self,content):
        """Generates a PDF document from an XML document inside a string.
        
        The document can be specified by a string containing the content of the document.
        
        param string content A string containing the content of the XML document.
        
        return string The PDF document as a base64encoded binary string.
        
        see renderDocumentFromURL()
        see renderDocumentFromByteArray()
        see renderDocumentFromContentAsArray()"""
        in0=content
        in1=self.PDFreactorConfiguration.in1
        args = {"in0" : in0, "in1" : in1}
        
        self.resp = self.client.ROCall("renderDocumentFromContent",args)
        return self.resp["pdf"]
        
    def renderDocumentFromURLAsArray(self,url):
        """Generates an array of byte-arrays each containing an image representing 
        one page of the document from an HTML or XML document at a URL.
        
        param string url A URL pointing to the input document.
         
        return array An array of byte-arrays each containing an image representing one page of the document.
        
        see renderDocumentFromByteArrayAsArray()
        see renderDocumentFromContentAsArray()
        see renderDocumentFromURL()"""
        in0=url
        in1=self.PDFreactorConfiguration.in1
        args = {"in0" : in0, "in1" : in1}
        
        self.resp = self.client.ROCall("renderDocumentFromURLAsArray", args)
        return self.resp["outputArray"]
    
    def renderDocumentFromByteArrayAsArray(self,byteArray):
        """Generates an array of byte-arrays each containing an image representing 
        one page of the document from an HTML or XML document inside a byte-array.
        
        param array An array containing the content of the HTML or XML document.
         
        return array An array of byte-arrays each containing an image representing one page of the document.
        
        see renderDocumentFromURLAsArray()
        see renderDocumentFromContentAsArray()
        see renderDocumentFromByteArray()"""
        in0=byteArray
        in1=self.PDFreactorConfiguration.in1
        args = {"in0" : in0, "in1" : in1}
        
        self.resp = self.client.ROCall("renderDocumentFromByteArrayAsArray", args)
        return self.resp["outputArray"]
    
    def renderDocumentFromContentAsArray(self,content):
        """Generates an array of byte-arrays each containing an image representing 
        one page of the document from an HTML or XML document inside a String.
        
        param content A String containing the content of the HTML or XML document.
         
        return array An array of byte-arrays each containing an image representing one page of the document.
        
        see renderDocumentFromURLAsArray()
        see renderDocumentFromByteArrayAsArray()
        see renderDocumentFromContent()"""
        in0=content
        in1=self.PDFreactorConfiguration.in1
        args = {"in0" : in0, "in1" : in1}
        
        self.resp = self.client.ROCall("renderDocumentFromContentAsArray", args)
        return self.resp["outputArray"]
    
    #=================
    # Logging methods
    #=================
        
    def getError(self):
        """Returns the error messages generated during rendering.
    
        return string The message string."""
        
        return self.resp["error"]
        
    def getLog(self):
        """Returns the log messages generated during rendering based on the log level.
    
        return string The log string.
        
        see setLogLevel()"""
        
        return self.resp["log"]
    
    def getExceedingContents(self):
        """Provides information about content exceeding its page or parent. Depends on the mode set via setLogExceedingContent(int, int).
        
        return an array of ExceedingContent objects 
        or None if the logging of exceeding content was not enabled 
        or no conversion was run, yet.
        
        return ExceedingContent[] The exceeding contents."""
        
        return self.resp["exceedingContents"]
    
    def getNumberOfPages(self,value):
        """Returns the number of pages of the document after conversion.
        
        The result returned by this method will only be correct if the 
        document has already been laid out by one of the render methods:
        
        see renderDocumentFromURLAsArray()
        see renderDocumentFromByteArrayAsArray()
        see renderDocumentFromContent()
        
        param boolean pdf If True, returns the number of pages of the 
                          resulting PDF (including, e.g., merge operations), otherwise
                          it will return the number pages of the laid out input 
                          document."""
        
        if value == True:
            return self.resp["numberOfPagesPDF"]
        else:
            return self.resp["numberOfPages"]
        
    #=======================
    # Output format methods
    #=======================
    def setOutputFormat(self,format,outputWidth,outputHeight):
        """Sets the output format. The default value is 'PDF'.
        For image formats the width or height in pixels must be specified. 
        When either dimension is <1 it is computed based on the other dimension and the aspect ratio of the input document.
        
        param format the output format. See 'OUTPUT_FORMAT_' constants
        param outputWidth The width of the output in pixels (image formats only). Values <1 will be computed based on the specified height and the aspect ratio of the input document.
        param outputHeight The height of the output in pixels (image formats only). Values <1 will be computed based on the specified width and the aspect ratio of the input document.
        
        see OUTPUT_FORMAT_PDF
        see OUTPUT_FORMAT_JPEG
        see OUTPUT_FORMAT_PNG
        see OUTPUT_FORMAT_PNG_TRANSPARENT
        see OUTPUT_FORMAT_BMP
        see OUTPUT_FORMAT_GIF
        see OUTPUT_FORMAT_PNG_AI
        see OUTPUT_FORMAT_PNG_TRANSPARENT_AI
        see OUTPUT_FORMAT_TIFF_LZW
        see OUTPUT_FORMAT_TIFF_PACKBITS
        see OUTPUT_FORMAT_TIFF_UNCOMPRESSED
        see OUTPUT_FORMAT_TIFF_CCITT_1D
        see OUTPUT_FORMAT_TIFF_CCITT_GROUP_3
        see OUTPUT_FORMAT_TIFF_CCITT_GROUP_4"""
        self.PDFreactorConfiguration.in1["outputFormat"] = format
        self.PDFreactorConfiguration.in1["outputWidth"] = outputWidth
        self.PDFreactorConfiguration.in1["outputHeight"] = outputHeight
        
class confObj:
    """Used only internaly. Do not use!"""
    def __init__(self):
        self.in1 = {}
        self.in1["version"] = "6.3"
        self.in1["licenseKey"] = None
        self.in1["disableFontRegistration"] = False
        self.in1["cacheFonts"] = False
        self.in1["fontCachePath"] = None
        self.in1["fontDirectory"] = None
        self.in1["fontDirectories"] = None
        self.in1["fonts"] = None
        self.in1["fontAliases"] = None
        self.in1["logLevel"] = 4
        self.in1["baseURL"] = None
        self.in1["XSLTMode"] = False
        self.in1["encoding"] = None
        self.in1["cleanupTool"] = 2
        self.in1["documentType"] = 0
        self.in1["postTransformationDocumentType"] = 0
        self.in1["userStyleSheets"] = None
        self.in1["XSLTStyleSheets"] = None
        self.in1["userScripts"] = None
        self.in1["author"] = None
        self.in1["creator"] = None
        self.in1["keywords"] = None
        self.in1["title"] = None
        self.in1["subject"] = None
        self.in1["customDocumentProperties"] = []
        self.in1["attachments"] = None
        self.in1["documentDefaultLanguage"] = None
        self.in1["encryption"] = 0
        self.in1["fullCompression"] = False
        self.in1["ownerPassword"] = None
        self.in1["userPassword"] = None
        self.in1["addLinks"] = False
        self.in1["addBookmarks"] = False
        self.in1["addTags"] = False
        self.in1["addPreviewImages"] = False
        self.in1["addAttachments"] = False
        self.in1["addOverprint"] = False
        self.in1["printDialogPrompt"] = False
        self.in1["appendLog"] = False
        self.in1["allowAnnotations"] = False
        self.in1["allowAssembly"] = False
        self.in1["allowCopy"] = False
        self.in1["allowDegradedPrinting"] = False
        self.in1["allowFillIn"] = False
        self.in1["allowModifyContents"] = False
        self.in1["allowPrinting"] = False
        self.in1["allowScreenReaders"] = False
        self.in1["javaScriptMode"] = 0
        self.in1["mergeURL"] = None
        self.in1["mergeURLs"] = None
        self.in1["mergeByteArray"] = None
        self.in1["mergeByteArrays"] = None
        self.in1["mergeMode"] = 0
        self.in1["viewerPreferences"] = 0
        self.in1["conformance"] = -1
        self.in1["defaultColorSpace"] = 0
        self.in1["outputIntentIdentifier"] = None
        self.in1["outputIntentICCProfileURL"] = None
        self.in1["outputIntentICCProfileData"] = None
        self.in1["processingPreferences"] = 0
        self.in1["overlayRepeat"] = 0
        self.in1["disableFontEmbedding"] = False
        self.in1["fontFallback"] = None
        self.in1["pixelsPerInch"] = 0
        self.in1["pixelsPerInchShrinkToFit"] = False
        self.in1["pagesPerSheetCols"] = 0
        self.in1["pagesPerSheetRows"] = 0
        self.in1["pagesPerSheetSheetSize"] = None
        self.in1["pagesPerSheetSheetMargin"] = None
        self.in1["pagesPerSheetSpacing"] = None
        self.in1["pagesPerSheetDirection"] = 0
        self.in1["pageOrder"] = None
        self.in1["bookletSheetSize"] = None
        self.in1["bookletSheetMargin"] = None
        self.in1["bookletRTL"] = False
        self.in1["authenticationUsername"] = None
        self.in1["authenticationPassword"] = None
        self.in1["requestHeaderMap"] = []
        self.in1["cookies"] = []
        self.in1["signPdfKeystoreURL"] = None
        self.in1["signPdfKeyAlias"] = None
        self.in1["signPdfKeystorePassword"] = None
        self.in1["signPdfKeystoreType"] = None
        self.in1["signPdfSigningMode"] = 0
        self.in1["throwLicenseExceptions"] = False
        self.in1["logExceedingContentAnalyze"] = -1
        self.in1["logExceedingContentAgainst"] = -1
        self.in1["bookletModeEnabled"] = False
        self.in1["httpsMode"] = 0
        self.in1["outputFormat"] = 0
        self.in1["outputWidth"] = 0
        self.in1["outputHeight"] = 0
        self.in1["continuousWidth"] = 0
        self.in1["continuousHeight"] = 0

class ROClient:
    def __init__(self, host, port, destination, debug = False):
        self.host = host
        self.port = port
        self.destination = destination
        self.debug = debug
        self.result = {}
        self.result["pdf"] = None
        self.result["outputArray"] = None
    
    def ROCall(self, method,args):
        generatedXML = self.generateXML(method,args)
        
        if self.debug:
            print "Content-Type: text/html\n"
            print "XML-Request: <br/><br/><pre>"
            print cgi.escape(generatedXML)
            print "</pre>"
        
        url = "http://"+self.host+":"+str(self.port)+self.destination
        print url
        headers = { "SOAPAction" : "", "Content-Length" :  str(len(generatedXML)), "Content-Type" : "text/xml; charset=UTF-8" }
        
        req = urllib2.Request(url, None, headers)
        req.add_data(generatedXML)
        response = urllib2.urlopen(req)
        xmlresult = response.read()
        
        if self.debug:
            print "XML-Response: <br/><br/><pre>"
            print cgi.escape(xmlresult)
            print "</pre>"
        
        xmldoc = minidom.parseString(xmlresult)
        
        outputArrayElement = xmldoc.getElementsByTagName('outputArray')
        pdfElement = xmldoc.getElementsByTagName('PDF')
        errorElement = xmldoc.getElementsByTagName('error')
        logElement = xmldoc.getElementsByTagName('log')
        numberOfPagesElement = xmldoc.getElementsByTagName('numberOfPages')
        numberOfPagesPDFElement = xmldoc.getElementsByTagName('numberOfPagesPDF')
        exceedingContentsElement = xmldoc.getElementsByTagName('exceedingContents')
        
        if pdfElement[0].firstChild != None:
            if pdfElement[0].firstChild.data != "":
                self.result["pdf"] = binascii.a2b_base64(pdfElement[0].firstChild.data)
            else:
                self.result["pdf"] = None
        else:
            self.result["pdf"] = None
            
        if errorElement[0].firstChild != None:
            if errorElement[0].firstChild.data != "":
                self.result["error"] = errorElement[0].firstChild.data
            else:
                self.result["error"] = None
        else:
            self.result["error"] = None
        
        if logElement[0].firstChild != None:
            if logElement[0].firstChild.data != "":
                self.result["log"] = logElement[0].firstChild.data
            else:
                self.result["log"] = None
        else:
            self.result["log"] = None
        
        if numberOfPagesElement[0].firstChild != None:
            if numberOfPagesElement[0].firstChild.data != "":
                self.result["numberOfPages"] = numberOfPagesElement[0].firstChild.data
            else:
                self.result["numberOfPages"] = None
        else:
            self.result["numberOfPages"] = None
            
        if numberOfPagesPDFElement[0].firstChild != None:
            if numberOfPagesPDFElement[0].firstChild.data != "":
                self.result["numberOfPagesPDF"] = numberOfPagesPDFElement[0].firstChild.data
            else:
                self.result["numberOfPagesPDF"] = None
        else:
            self.result["numberOfPagesPDF"] = None
            
        if outputArrayElement.length > 0:
            self.result["outputArray"] = []
            for elem in outputArrayElement[0].childNodes:
                self.result["outputArray"].append(binascii.a2b_base64(elem.firstChild.firstChild.data))
        else:
            self.result["outputArray"] = None
        
        if exceedingContentsElement.length > 0:
            self.result["exceedingContents"] = []
            for i in range(1, exceedingContentsElement.length):
                if exceedingContentsElement[i] != None:
                    exceedingContent = ExceedingContent()
                    for elem in exceedingContentsElement[i].childNodes:
                        if elem.nodeName == 'bottom':
                            exceedingContent.bottom = elem.firstChild.data
                        elif elem.nodeName == 'box':
                            exceedingContent.box = elem.firstChild.data
                        elif elem.nodeName == 'description':
                            exceedingContent.description = elem.firstChild.data
                        elif elem.nodeName == 'left':
                            exceedingContent.left = elem.firstChild.data
                        elif elem.nodeName == 'pageNumber':
                            exceedingContent.pageNumber = elem.firstChild.data
                        elif elem.nodeName == 'right':
                            exceedingContent.right = elem.firstChild.data
                        elif elem.nodeName == 'top':
                            exceedingContent.top = elem.firstChild.data
                        elif elem.nodeName == 'html':
                            exceedingContent.html = elem.firstChild.data
                        elif elem.nodeName == 'pageLeft':
                            exceedingContent.pageLeft = elem.firstChild.data
                        elif elem.nodeName == 'pageTop':
                            exceedingContent.pageTop = elem.firstChild.data
                        elif elem.nodeName == 'pageRight':
                            exceedingContent.pageRight = elem.firstChild.data
                        elif elem.nodeName == 'pageBottom':
                            exceedingContent.pageBottom = elem.firstChild.data
                        elif elem.nodeName == 'containerLeft':
                            exceedingContent.containerLeft = elem.firstChild.data
                        elif elem.nodeName == 'containerTop':
                            exceedingContent.containerTop = elem.firstChild.data
                        elif elem.nodeName == 'containerRight':
                            exceedingContent.containerRight = elem.firstChild.data
                        elif elem.nodeName == 'containerBottom':
                            exceedingContent.containerBottom = elem.firstChild.data
                        elif elem.nodeName == 'exceedingBoxLeft':
                            exceedingContent.exceedingBoxLeft = elem.firstChild.data
                        elif elem.nodeName == 'exceedingBoxTop':
                            exceedingContent.exceedingBoxTop = elem.firstChild.data
                        elif elem.nodeName == 'exceedingBoxRight':
                            exceedingContent.exceedingBoxRight = elem.firstChild.data
                        elif elem.nodeName == 'exceedingBoxBottom':
                            exceedingContent.exceedingBoxBottom = elem.firstChild.data
                        elif elem.nodeName == 'summary':
                            exceedingContent.summary = elem.firstChild.data
                    self.result["exceedingContents"].append(exceedingContent)
        else:
            self.result["exceedingContents"] = None
        
        return self.result
    
    def generateXML(self, method, args):
        self.xml = "<SOAP-ENV:Envelope  xmlns:SOAP-ENV='http://schemas.xmlsoap.org/soap/envelope/' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:SOAP-ENC='http://schemas.xmlsoap.org/soap/encoding/' SOAP-ENV:encodingStyle='http://schemas.xmlsoap.org/soap/encoding/'><SOAP-ENV:Body>"
        self.xml += "<"+method+">"
        
        if method == "renderDocumentFromByteArray":
            self.xml += "<in0 xsi:type='xsd:base64Binary'>"+args['in0']+"</in0>"
        else:
            self.xml += "<in0 xsi:type='string'>"+cgi.escape(args['in0'])+"</in0>"
        
        self.xml += "<in1>"
        for key in args["in1"].keys():
            
            if (args["in1"][key] is False):
                args["in1"][key] = "false"
                varType = "boolean"
            
            elif (args["in1"][key] is True):
                args["in1"][key] = "true"
                varType = "boolean"
            
            elif (type(args["in1"][key]) == type(int())):
                varType = "int"
                args["in1"][key] = str(args["in1"][key])
            
            elif type(args["in1"][key]) == type(str()):
                varType = "string"
                
            else:
                varType = type(args["in1"][key])
                
            if type(args["in1"][key]) == type(list()):
                self.xml += "<"+key+">"
                for i in range(0, len(args["in1"][key])):
                    if type(args["in1"][key][i]) == type(str()):
                        if key == "mergeByteArrays":
                            self.xml += "<item xsi:type=\"xsd:base64Binary\">"+args["in1"][key][i]+"</item>"
                        else:
                            self.xml += "<item xsi:type=\"xsd:string\">"+args["in1"][key][i]+"</item>"
                    elif type(args["in1"][key][i]) == type(list()):
                        self.xml += "<item>"
                        self.xml += "<item xsi:type=\"string\">"+args["in1"][key][i][0]+"</item>"
                        self.xml += "<item xsi:type=\"string\">"+args["in1"][key][i][1]+"</item>"
                        self.xml += "</item>"
                    else:
                        self.xml += "<item>"
                        for ussKey in args["in1"][key][i].keys():
                            if type(args["in1"][key][i][ussKey]) == type(bool()):
                                self.xml += "<"+ussKey+" xsi:type=\"boolean\">"+str.lower(str(args["in1"][key][i][ussKey]))+"</"+ussKey+">"
                            elif ussKey == "data":
                                if args["in1"][key][i][ussKey] == None:
                                    self.xml += "<"+ussKey+" xsi:nil=\"true\" />"
                                else:
                                    self.xml += "<"+ussKey+" xsi:type=\"xsd:base64Binary\">"+args["in1"][key][i][ussKey]+"</"+ussKey+">"
                            else:
                                self.xml += "<"+ussKey+" xsi:type=\"xsd:string\">"+cgi.escape(str(args["in1"][key][i][ussKey]))+"</"+ussKey+">"
                        self.xml += "</item>"
                self.xml += "</"+key+">"
             
            elif args["in1"][key] == None or args["in1"][key] == "":
                self.xml += "<"+key+" xsi:nil=\"true\" />"
            elif key == "mergeByteArray" or key == "outputIntentICCProfileData":
                self.xml += "<"+key+" xsi:type=\"xsd:base64Binary\">"+args["in1"][key]+"</"+key+">"
            elif varType == "string":
                self.xml += "<"+key+" xsi:type=\""+str(varType)+"\">"+cgi.escape(str(args["in1"][key]))+"</"+key+">"
            else:
                self.xml += "<"+key+" xsi:type=\""+str(varType)+"\">"+str(args["in1"][key])+"</"+key+">"
        
        
        self.xml += "</in1>"
        self.xml += "</"+method+">"
        self.xml += "</SOAP-ENV:Body></SOAP-ENV:Envelope>"
        
        return self.xml
    
class ExceedingContent:
    """Object that describes one instance of content exceeding its page or parent."""
    def __init__(self):
        self.pageNumber = 0
        self.right = False
        self.bottom = False
        self.left = False
        self.top = False
        self.description = None
        self.box = False
        self.html = None
        self.pageLeft = False
        self.pageTop = False
        self.pageRight = False
        self.pageBottom = False
        self.containerLeft = False
        self.containerTop = False
        self.containerRight = False
        self.containerBottom = False
        self.exceedingBoxLeft = False
        self.exceedingBoxTop = False
        self.exceedingBoxRight = False
        self.exceedingBoxBottom = False
        self.summary = None
        
    def getPageNumber(self):
        """Returns the number of the page that contains the exceeding content."""
        return self.pageNumber
    
    def isRight(self):
        """Returns whether the content exceeds the page to the right."""
        return self.right
    
    def isBottom(self):
        """Returns whether the content exceeds the page at the bottom."""
        return self.bottom
    
    def isLeft(self):
        """Returns whether the content exceeds the page to the left."""
        return self.left
    
    def isTop(self):
        """Returns whether the content exceeds the page at the top."""
        return self.top
    
    def getDescription(self):
        """Returns a description of the content. In case of text content, the text is returned. In case of 
        images the URL is returned if available."""
        return self.description
    
    def isBox(self):
        """Returns whether the exceeding content is a box instead of text or image content."""
        return self.box
    
    def getHtml(self):
        """Returns the HTML of the box that contains the exceeding content."""
        return self.html
    
    def getPageLeft(self):
        """Returns the left coordinate of the the page in pixels."""
        return self.pageLeft
    
    def getPageTop(self):
        """Returns the top coordinate of the the page in pixels."""
        return self.pageTop
    
    def getPageRight(self):
        """Returns the right coordinate of the the page in pixels."""
        return self.pageRight
    
    def getPageBottom(self):
        """Returns the bottom coordinate of the the page in pixels."""
        return self.pageBottom
    
    def getContainerLeft(self):
        """Returns the left coordinate of the the container box in the page in pixels. Depending on the settings this box may be the page."""
        return self.containerLeft
    
    def getContainerTop(self):
        """Returns the top coordinate of the the container box in the page in pixels. Depending on the settings this box may be the page."""
        return self.containerTop
    
    def getContainerRight(self):
        """Returns the right coordinate of the the container box in the page in pixels. Depending on the settings this box may be the page."""
        return self.containerRight
    
    def getContainerBottom(self):
        """Returns the bottom coordinate of the the container box in the page in pixels. Depending on the settings this box may be the page."""
        return self.containerBottom
    
    def getExceedingBoxLeft(self):
        """Returns the left coordinate of the the exceeding box in the page in pixels."""
        return self.exceedingBoxLeft
    
    def getExceedingBoxTop(self):
        """Returns the top coordinate of the the exceeding box in the page in pixels."""
        return self.exceedingBoxTop
    
    def getExceedingBoxRight(self):
        """Returns the right coordinate of the the exceeding box in the page in pixels."""
        return self.exceedingBoxRight
    
    def getExceedingBoxBottom(self):
        """Returns the bottom coordinate of the the exceeding box in the page in pixels."""
        return self.exceedingBoxBottom
    
    def getSummary(self):
        """Returns a summary of this exceeding content object."""
        return self.summary