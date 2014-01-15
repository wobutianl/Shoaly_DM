# -*- coding: utf-8 -*-
import sys, time, math, os, os.path

import wx
import mongo_bll
_ = wx.GetTranslation
import wx.propgrid as wxpg


############################################################################
#
# TEST RELATED CODE AND VARIABLES
#
############################################################################

default_object_content2 = """\
object.title = "Object Title"
object.index = 1
object.PI = %f
object.wxpython_rules = True
"""%(math.pi)

default_object_content1 = """\

#
# Note that the results of autofill will appear on the second page.

#
# Set number of iterations appropriately to test performance
iterations = 100

#
# Test result for 100,000 iterations on Athlon XP 2000+:
#
# Time spent per property: 0.054ms
# Memory allocated per property: ~350 bytes (includes Python object)
#

for i in range(0,iterations):
    setattr(object,'title%i'%i,"Object Title")
    setattr(object,'index%i'%i,1)
    setattr(object,'PI%i'%i,3.14)
    setattr(object,'wxpython_rules%i'%i,True)
"""


############################################################################
#
# CUSTOM PROPERTY SAMPLES
#
############################################################################


class ValueObject:
    def __init__(self):
        pass


class IntProperty2(wxpg.PyProperty):
    """\
    This is a simple re-implementation of wxIntProperty.
    """
    def __init__(self, label, name = wxpg.LABEL_AS_NAME, value=0):
        wxpg.PyProperty.__init__(self, label, name)
        self.SetValue(value)

    def GetClassName(self):
        """\
        This is not 100% necessary and in future is probably going to be
        automated to return class name.
        """
        return "IntProperty2"

    def GetEditor(self):
        return "TextCtrl"

    def ValueToString(self, value, flags):
        return str(value)

    def StringToValue(self, s, flags):
        """ If failed, return False or (False, None). If success, return tuple
            (True, newValue).
        """
        try:
            v = int(s)
            if self.GetValue() != v:
                return (True, v)
        except (ValueError, TypeError):
            if flags & wxpg.PG_REPORT_ERROR:
                wx.MessageBox("Cannot convert '%s' into a number."%s, "Error")
        return False

    def IntToValue(self, v, flags):
        """ If failed, return False or (False, None). If success, return tuple
            (True, newValue).
        """
        if (self.GetValue() != v):
            return (True, v)
        return False

    def ValidateValue(self, value, validationInfo):
        """ Let's limit the value to range -10000 and 10000.
        """
        # Just test this function to make sure validationInfo and
        # wxPGVFBFlags work properly.
        oldvfb__ = validationInfo.GetFailureBehavior()

        # Mark the cell if validaton failred
        validationInfo.SetFailureBehavior(wxpg.PG_VFB_MARK_CELL)

        if value < -10000 or value > 10000:
            return False

        return (True, value)


class SizeProperty(wxpg.PyProperty):
    """ Demonstrates a property with few children.
    """
    def __init__(self, label, name = wxpg.LABEL_AS_NAME, value=wx.Size(0, 0)):
        wxpg.PyProperty.__init__(self, label, name)

        value = self._ConvertValue(value)

        self.AddPrivateChild( wxpg.IntProperty("X", value=value.x) )
        self.AddPrivateChild( wxpg.IntProperty("Y", value=value.y) )

        self.m_value = value

    def GetClassName(self):
        return self.__class__.__name__

    def GetEditor(self):
        return "TextCtrl"

    def RefreshChildren(self):
        size = self.m_value
        self.Item(0).SetValue( size.x )
        self.Item(1).SetValue( size.y )

    def _ConvertValue(self, value):
        """ Utility convert arbitrary value to a real wx.Size.
        """
        from operator import isSequenceType
        if isinstance(value, wx.Point):
            value = wx.Size(value.x, value.y)
        elif isSequenceType(value):
            value = wx.Size(*value)
        return value

    def ChildChanged(self, thisValue, childIndex, childValue):
        # FIXME: This does not work yet. ChildChanged needs be fixed "for"
        #        wxPython in wxWidgets SVN trunk, and that has to wait for
        #        2.9.1, as wxPython 2.9.0 uses WX_2_9_0_BRANCH.
        size = self._ConvertValue(self.m_value)
        if childIndex == 0:
            size.x = childValue
        elif childIndex == 1:
            size.y = childValue
        else:
            raise AssertionError

        return size


class DirsProperty(wxpg.PyArrayStringProperty):
    """ Sample of a custom custom ArrayStringProperty.

        Because currently some of the C++ helpers from wxArrayStringProperty
        and wxProperytGrid are not available, our implementation has to quite
        a bit 'manually'. Which is not too bad since Python has excellent
        string and list manipulation facilities.
    """
    def __init__(self, label, name = wxpg.LABEL_AS_NAME, value=[]):
        wxpg.PyArrayStringProperty.__init__(self, label, name, value)

        # Set default delimiter
        self.SetAttribute("Delimiter", ',')

    def GetEditor(self):
        return "TextCtrlAndButton"

    def ValueToString(self, value, flags):
        return self.m_display

    def OnSetValue(self):
        self.GenerateValueAsString()

    def DoSetAttribute(self, name, value):
        # Proper way to call same method from super class
        retval = self.CallSuperMethod("DoSetAttribute", name, value)

        #
        # Must re-generate cached string when delimiter changes
        if name == "Delimiter":
            self.GenerateValueAsString(delim=value)

        return retval

    def GenerateValueAsString(self, delim=None):
        """ This function creates a cached version of displayed text
            (self.m_display).
        """
        if not delim:
            delim = self.GetAttribute("Delimiter")
            if not delim:
                delim = ','

        ls = self.GetValue()
        if delim == '"' or delim == "'":
            text = ' '.join(['%s%s%s'%(delim,a,delim) for a in ls])
        else:
            text = ', '.join(ls)
        self.m_display = text

    def StringToValue(self, text, argFlags):
        """ If failed, return False or (False, None). If success, return tuple
            (True, newValue).
        """
        delim = self.GetAttribute("Delimiter")
        if delim == '"' or delim == "'":
            # Proper way to call same method from super class
            return self.CallSuperMethod("StringToValue", text, 0)
        v = [a.strip() for a in text.split(delim)]
        return (True, v)

    def OnEvent(self, propgrid, primaryEditor, event):
        if event.GetEventType() == wx.wxEVT_COMMAND_BUTTON_CLICKED:
            dlg = wx.DirDialog(propgrid,
                               _("Select a directory to be added to "
                                 "the list:"))

            if dlg.ShowModal() == wx.ID_OK:
                new_path = dlg.GetPath()
                old_value = self.m_value
                if old_value:
                    new_value = list(old_value)
                    new_value.append(new_path)
                else:
                    new_value = [new_path]
                self.SetValueInEvent(new_value)
                retval = True
            else:
                retval = False

            dlg.Destroy()
            return retval

        return False


class PyObjectPropertyValue:
    """\
    Value type of our sample PyObjectProperty. We keep a simple dash-delimited
    list of string given as argument to constructor.
    """
    def __init__(self, s=None):
        try:
            self.ls = [a.strip() for a in s.split('-')]
        except:
            self.ls = []

    def __repr__(self):
        return ' - '.join(self.ls)


class PyObjectProperty(wxpg.PyProperty):
    """\
    Another simple example. This time our value is a PyObject.

    NOTE: We can't return an arbitrary python object in DoGetValue. It cannot
          be a simple type such as int, bool, double, or string, nor an array
          or wxObject based. Dictionary, None, or any user-specified Python
          class is allowed.
    """
    def __init__(self, label, name = wxpg.LABEL_AS_NAME, value=None):
        wxpg.PyProperty.__init__(self, label, name)
        self.SetValue(value)

    def GetClassName(self):
        return self.__class__.__name__

    def GetEditor(self):
        return "TextCtrl"

    def ValueToString(self, value, flags):
        return repr(value)

    def StringToValue(self, s, flags):
        """ If failed, return False or (False, None). If success, return tuple
            (True, newValue).
        """
        v = PyObjectPropertyValue(s)
        return (True, v)


class SampleMultiButtonEditor(wxpg.PyTextCtrlEditor):
    def __init__(self):
        wxpg.PyTextCtrlEditor.__init__(self)

    def CreateControls(self, propGrid, property, pos, sz):
        # Create and populate buttons-subwindow
        buttons = wxpg.PGMultiButton(propGrid, sz)

        # Add two regular buttons
        buttons.AddButton("...")
        buttons.AddButton("A")
        # Add a bitmap button
        buttons.AddBitmapButton(wx.ArtProvider.GetBitmap(wx.ART_FOLDER))
        
        # Create the 'primary' editor control (textctrl in this case)
        wnd = self.CallSuperMethod("CreateControls",
                                   propGrid,
                                   property,
                                   pos,
                                   buttons.GetPrimarySize())

        # Finally, move buttons-subwindow to correct position and make sure
        # returned wxPGWindowList contains our custom button list.
        buttons.Finalize(propGrid, pos);

        # We must maintain a reference to any editor objects we created
        # ourselves. Otherwise they might be freed prematurely. Also,
        # we need it in OnEvent() below, because in Python we cannot "cast"
        # result of wxPropertyGrid.GetEditorControlSecondary() into
        # PGMultiButton instance.
        self.buttons = buttons

        return (wnd, buttons)

    def OnEvent(self, propGrid, prop, ctrl, event):
        if event.GetEventType() == wx.wxEVT_COMMAND_BUTTON_CLICKED:
            buttons = self.buttons
            evtId = event.GetId()

            if evtId == buttons.GetButtonId(0):
                # Do something when the first button is pressed
                wx.LogDebug("First button pressed");
                return False  # Return false since value did not change
            if evtId == buttons.GetButtonId(1):
                # Do something when the second button is pressed
                wx.MessageBox("Second button pressed");
                return False  # Return false since value did not change
            if evtId == buttons.GetButtonId(2):
                # Do something when the third button is pressed
                wx.MessageBox("Third button pressed");
                return False  # Return false since value did not change

        return self.CallSuperMethod("OnEvent", propGrid, prop, ctrl, event)


class SingleChoiceDialogAdapter(wxpg.PyEditorDialogAdapter):
    """ This demonstrates use of wxpg.PyEditorDialogAdapter.
    """
    def __init__(self, choices):
        wxpg.PyEditorDialogAdapter.__init__(self)
        self.choices = choices

    def DoShowDialog(self, propGrid, property):
        s = wx.GetSingleChoice("Message", "Caption", self.choices)

        if s:
            self.SetValue(s)
            return True

        return False;


class SingleChoiceProperty(wxpg.PyStringProperty):
    def __init__(self, label, name=wxpg.LABEL_AS_NAME, value=''):
        wxpg.PyStringProperty.__init__(self, label, name, value)

        # Prepare choices
        dialog_choices = []
        dialog_choices.append("Cat");
        dialog_choices.append("Dog");
        dialog_choices.append("Gibbon");
        dialog_choices.append("Otter");

        self.dialog_choices = dialog_choices

    def GetEditor(self):
        # Set editor to have button
        return "TextCtrlAndButton"

    def GetEditorDialog(self):
        # Set what happens on button click
        return SingleChoiceDialogAdapter(self.dialog_choices)


class TrivialPropertyEditor(wxpg.PyEditor):
    """\
    This is a simple re-creation of TextCtrlWithButton. Note that it does
    not take advantage of wx.TextCtrl and wx.Button creation helper functions
    in wx.PropertyGrid.
    """
    def __init__(self):
        wxpg.PyEditor.__init__(self)

    def CreateControls(self, propgrid, property, pos, sz):
        """ Create the actual wxPython controls here for editing the
            property value.

            You must use propgrid.GetPanel() as parent for created controls.

            Return value is either single editor control or tuple of two
            editor controls, of which first is the primary one and second
            is usually a button.
        """
        try:
            x, y = pos
            w, h = sz
            h = 64 + 6

            # Make room for button
            bw = propgrid.GetRowHeight()
            w -= bw

            s = property.GetDisplayedString();

            tc = wx.TextCtrl(propgrid.GetPanel(), wxpg.PG_SUBID1, s,
                             (x,y), (w,h),
                             wx.TE_PROCESS_ENTER)
            btn = wx.Button(propgrid.GetPanel(), wxpg.PG_SUBID2, '...',
                            (x+w, y),
                            (bw, h), wx.WANTS_CHARS)
            return (tc, btn)
        except:
            import traceback
            print(traceback.print_exc())

    def UpdateControl(self, property, ctrl):
        ctrl.SetValue(property.GetDisplayedString())

    def DrawValue(self, dc, rect, property, text):
        if not property.IsValueUnspecified():
            dc.DrawText(property.GetDisplayedString(), rect.x+5, rect.y)

    def OnEvent(self, propgrid, property, ctrl, event):
        """ Return True if modified editor value should be committed to
            the property. To just mark the property value modified, call
            propgrid.EditorsValueWasModified().
        """
        if not ctrl:
            return False

        evtType = event.GetEventType()

        if evtType == wx.wxEVT_COMMAND_TEXT_ENTER:
            if propgrid.IsEditorsValueModified():
                return True
        elif evtType == wx.wxEVT_COMMAND_TEXT_UPDATED:
            #
            # Pass this event outside wxPropertyGrid so that,
            # if necessary, program can tell when user is editing
            # a textctrl.
            event.Skip()
            event.SetId(propgrid.GetId())

            propgrid.EditorsValueWasModified()
            return False

        return False

    def GetValueFromControl(self, property, ctrl):
        """ Return tuple (wasSuccess, newValue), where wasSuccess is True if
            different value was acquired succesfully.
        """
        tc = ctrl
        textVal = tc.GetValue()

        if property.UsesAutoUnspecified() and not textVal:
            return (True, None)

        res, value = property.StringToValue(textVal,
                                            wxpg.PG_EDITABLE_VALUE)

        # Changing unspecified always causes event (returning
        # True here should be enough to trigger it).
        if not res and value is None:
            res = True

        return (res, value)

    def SetValueToUnspecified(self, property, ctrl):
        ctrl.Remove(0,len(ctrl.GetValue()))

    def SetControlStringValue(self, property, ctrl, text):
        ctrl.SetValue(text)

    def OnFocus(self, property, ctrl):
        ctrl.SetSelection(-1,-1)
        ctrl.SetFocus()


class LargeImagePickerCtrl(wx.Panel):
    """\
    Control created and used by LargeImageEditor.
    """
    def __init__(self):
        pre = wx.PrePanel()
        self.PostCreate(pre)

    def Create(self, parent, id_, pos, size, style = 0):
        wx.Panel.Create(self, parent, id_, pos, size,
                        style | wx.BORDER_SIMPLE)
        img_spc = size[1]
        self.tc = wx.TextCtrl(self, -1, "", (img_spc,0), (2048,size[1]),
                              wx.BORDER_NONE)
        self.SetBackgroundColour(wx.WHITE)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.property = None
        self.bmp = None
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)

        whiteBrush = wx.Brush(wx.WHITE)
        dc.SetBackground(whiteBrush)
        dc.Clear()

        bmp = self.bmp
        if bmp:
            dc.DrawBitmap(bmp, 2, 2)
        else:
            dc.SetPen(wx.Pen(wx.BLACK))
            dc.SetBrush(whiteBrush)
            dc.DrawRectangle(2, 2, 64, 64)

    def RefreshThumbnail(self):
        """\
        We use here very simple image scaling code.
        """
        if not self.property:
            self.bmp = None
            return

        path = self.property.DoGetValue()

        if not os.path.isfile(path):
            self.bmp = None
            return

        image = wx.Image(path)
        image.Rescale(64, 64)
        self.bmp = wx.BitmapFromImage(image)

    def SetProperty(self, property):
        self.property = property
        self.tc.SetValue(property.GetDisplayedString())
        self.RefreshThumbnail()

    def SetValue(self, s):
        self.RefreshThumbnail()
        self.tc.SetValue(s)

    def GetLastPosition(self):
        return self.tc.GetLastPosition()


class LargeImageEditor(wxpg.PyEditor):
    """\
    Double-height text-editor with image in front.
    """
    def __init__(self):
        wxpg.PyEditor.__init__(self)

    def CreateControls(self, propgrid, property, pos, sz):
        try:
            x, y = pos
            w, h = sz
            h = 64 + 6

            # Make room for button
            bw = propgrid.GetRowHeight()
            w -= bw

            lipc = LargeImagePickerCtrl()
            if sys.platform.startswith('win'):
                lipc.Hide()
            lipc.Create(propgrid.GetPanel(), wxpg.PG_SUBID1, (x,y), (w,h))
            lipc.SetProperty(property)
            # Hmmm.. how to have two-stage creation without subclassing?
            #btn = wx.PreButton()
            #pre = wx.PreWindow()
            #self.PostCreate(pre)
            #if sys.platform == 'win32':
            #    btn.Hide()
            #btn.Create(propgrid, wxpg.PG_SUBID2, '...', (x2-bw,pos[1]),
            #           (bw,h), wx.WANTS_CHARS)
            btn = wx.Button(propgrid.GetPanel(), wxpg.PG_SUBID2, '...',
                            (x+w, y),
                            (bw, h), wx.WANTS_CHARS)
            return (lipc, btn)
        except:
            import traceback
            print(traceback.print_exc())

    def UpdateControl(self, property, ctrl):
        ctrl.SetValue(property.GetDisplayedString())

    def DrawValue(self, dc, rect, property, text):
        if not property.IsValueUnspecified():
            dc.DrawText(property.GetDisplayedString(), rect.x+5, rect.y)

    def OnEvent(self, propgrid, property, ctrl, event):
        """ Return True if modified editor value should be committed to
            the property. To just mark the property value modified, call
            propgrid.EditorsValueWasModified().
        """
        if not ctrl:
            return False

        evtType = event.GetEventType()

        if evtType == wx.wxEVT_COMMAND_TEXT_ENTER:
            if propgrid.IsEditorsValueModified():
                return True
        elif evtType == wx.wxEVT_COMMAND_TEXT_UPDATED:
            #
            # Pass this event outside wxPropertyGrid so that,
            # if necessary, program can tell when user is editing
            # a textctrl.
            event.Skip()
            event.SetId(propgrid.GetId())

            propgrid.EditorsValueWasModified()
            return False

        return False

    def GetValueFromControl(self, property, ctrl):
        """ Return tuple (wasSuccess, newValue), where wasSuccess is True if
            different value was acquired succesfully.
        """
        tc = ctrl.tc
        textVal = tc.GetValue()

        if property.UsesAutoUnspecified() and not textVal:
            return (None, True)

        res, value = property.StringToValue(textVal,
                                            wxpg.PG_EDITABLE_VALUE)

        # Changing unspecified always causes event (returning
        # True here should be enough to trigger it).
        if not res and value is None:
            res = True

        return (res, value)

    def SetValueToUnspecified(self, property, ctrl):
        ctrl.tc.Remove(0,len(ctrl.tc.GetValue()))

    def SetControlStringValue(self, property, ctrl, txt):
        ctrl.SetValue(txt)

    def OnFocus(self, property, ctrl):
        ctrl.tc.SetSelection(-1,-1)
        ctrl.tc.SetFocus()

    def CanContainCustomImage(self):
        return True


############################################################################
#
# MAIN PROPERTY GRID TEST PANEL
#
############################################################################
#datalinkValues = {}
#dbValues  = []
#listValues = []
class OnDataLinkView( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__(self, parent, wx.ID_ANY ,size=(700,400) , title = u"数据库连接")
        #self.log = log

        self.panel = panel = wx.Panel(self, wx.ID_ANY)
        #self.SetMinSize((700,400))
        topsizer = wx.BoxSizer(wx.VERTICAL)

        # Difference between using PropertyGridManager vs PropertyGrid is that
        # the manager supports multiple pages and a description box.
        self.pg = pg = wxpg.PropertyGridManager(panel,
                        style=wxpg.PG_SPLITTER_AUTO_CENTER |
                              wxpg.PG_AUTO_SORT |
                              wxpg.PG_DESCRIPTION |
                              wxpg.PG_TOOLBAR)

        # Show help as tooltips
        pg.SetExtraStyle(wxpg.PG_EX_HELP_AS_TOOLTIPS)    

        #
        # Let's use some simple custom editor
        #
        # NOTE: Editor must be registered *before* adding a property that
        # uses it.
        #if not getattr(sys, '_PropGridEditorsRegistered', False):
            #pg.RegisterEditor(TrivialPropertyEditor)
            #pg.RegisterEditor(SampleMultiButtonEditor)
            #pg.RegisterEditor(LargeImageEditor)
            ## ensure we only do it once
            #sys._PropGridEditorsRegistered = True

        #
        # Add properties
        #

        pg.AddPage( "Page 1 - Testing All" )

        pg.Append( wxpg.PropertyCategory("1 - Basic Properties")  )
        #pg.Append( wxpg.EditEnumProperty("EditEnum","EditEnumProperty",
                                                         #['A','B','C'],
                                                         #[0,1,2],
                                                         #"Text Not in List"))
        
        pg.Append( wxpg.IntProperty(label = u"端口", name = "port", value=27017 ))
        pg.Append( wxpg.StringProperty(u"计算机名",name = "pcname" ,value="localhost") )
        
        
        # When page is added, it will become the target page for AutoFill
        # calls (and for other property insertion methods as well)
        

        topsizer.Add(pg, 1, wx.EXPAND)
        # add some button 
        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        TestBtn = wx.Button(panel,-1,u"测试")
        TestBtn.Bind( wx.EVT_BUTTON, self.OnTestBtn )
        sureBtn = wx.Button(panel,-1,u"连接")
        sureBtn.Bind( wx.EVT_BUTTON, self.OnSureBtn )        
        CancelBtn = wx.Button(panel,-1,u"取消")
        CancelBtn.Bind( wx.EVT_BUTTON, self.OnCancelBtn )        
        rowsizer.Add((20, 20), 5, 0, 0)
        rowsizer.Add(TestBtn,0,0,0) 
        rowsizer.Add(sureBtn,0,0,0) 
        rowsizer.Add(CancelBtn,0,0,0)    
        
        topsizer.Add(rowsizer,0,wx.EXPAND)
        
        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        panel.SetSizer(topsizer)
        topsizer.SetSizeHints(panel)
        #topsizer.SetMinSize((600,300))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        
        self.value = ["a","b","c"]
        self.lens = [1,2,3,4]

    #----------------------------------------------------------------------
    def testLink(self ):
        """测试连接参数是否正确"""
        try:
            portvalue = self.pg.GetPropertyValue("port")
            pcname = self.pg.GetPropertyValue("pcname")
            self.datalink = mongo_bll.getConnection()

        except:
            return False
            
    #----------------------------------------------------------------------
    def OnTestBtn(self , event ):
        """测试按钮"""
        self.testLink()
        try:
            global dbValues
            dbValues = mongo_bll.getDB_names()
            print dbValues
            global listValues
            listValues = range(len(dbValues))
            self.pg.Append( wxpg.EditEnumProperty(u"数据库名","databaseName",
                                                                     dbValues , listValues,
                                                                     "Text Not in List"))                
        except:
            wx.MessageBox('Connection Error', 'Message', 
                        wx.OK | wx.ICON_ERROR)            
            
        
    #----------------------------------------------------------------------
    def OnSureBtn(self , event):
        """确定按钮"""
        global datalinkValues
        datalinkValues = self.pg.GetPropertyValues()
        global databaseName 
        databaseName = self.pg.GetPropertyValueAsString("databaseName")
        print datalinkValues
        self.Close()
        print "connect to mongodb"    
        
    #----------------------------------------------------------------------
    def OnCancelBtn(self , event):
        """取消按钮"""
        self.Close()
        print "connect to mongodb"
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = OnDataLinkView(None)
    frame.Show(True)
    app.MainLoop()
    
#a = {"attri1":value , "attri2":{"$in":["value1","value2"]} , "attri3": {"$slice":10}} ,{"attri1":1,"attri2":0} 