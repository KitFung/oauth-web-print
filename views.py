import flask_login as login
import flask_admin as admin
from flask_admin import helpers, expose
from flask import redirect, url_for, request, render_template

from loginform import LoginForm
from loginform import PrintingForm # for printing form
from flask_wtf import FlaskForm # for printing form
from werkzeug.utils import secure_filename # for printing form
import os # added for printing form

import stub as stub

import cups # main purpose

# some variables/functions for printing check
UPLOAD_FOLDER = '/tmp/oauth-web-print-uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 

# Create customized index view class that handles login & registration
class AdminIndexView(admin.AdminIndexView):
    
    def _stubs(self):
        self.nav = {
            "tasks" : stub.get_tasks(),
            "messages" : stub.get_messages_summary(),
            "alerts" : stub.get_alerts()
        }
        
        (cols, rows) = stub.get_adv_tables()
        (scols, srows, context) = stub.get_tables()
        
        self.tables = {
            "advtables" : { "columns" : cols, "rows" : rows },
            "table" : { "columns" : scols, "rows" : srows, "context" : context}
        }
        
        self.panelswells = {
            "accordion" : stub.get_accordion_items(),
            "tabitems" : stub.get_tab_items()
        }
            
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
            
        self._stubs()    
        self.header = "Dashboard"
        return render_template('sb-admin/pages/dashboard.html', admin_view=self)
    
    @expose('/blank')
    def blank(self):        
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
            
        self._stubs()    
        self.header = "Blank"
        return render_template('sb-admin/pages/blank.html', admin_view=self)
        
    @expose('/flot')
    def flot(self):        
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
            
        self._stubs()    
        self.header = "Flot Charts"
        return render_template('sb-admin/pages/flot.html', admin_view=self)

    @expose('/morris')
    def morris(self):        
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
            
        self._stubs()    
        self.header = "Morris Charts"
        return render_template('sb-admin/pages/morris.html', admin_view=self) 
        
    @expose('/tables')
    def tables(self):        
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
            
        self._stubs()    
        self.header = "Tables"
        return render_template('sb-admin/pages/tables.html', admin_view=self)

# FORMS: MODIFIED for printing        
    @expose('/forms', methods=('GET', 'POST'))
    def forms(self):        
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
            
        form = PrintingForm(request.form) #added
        self._stubs()    
        self.header = "Printing!"
        self._template_args['form'] = form #added


        # if POSTED and validated
        if request.method == 'POST' and form.validate_on_submit():
            file = request.files['file']

            # check file type is valid, e.g. XXX.pdf
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)

                # temp dir for uploading
                try:
                    os.stat(UPLOAD_FOLDER)
                except:
                    os.mkdir(UPLOAD_FOLDER)

                file.save(os.path.join(UPLOAD_FOLDER, filename))

                # print form.pagerange.data, form.side.data, form.numberup.data


                # set options

                options = {}
                # options: pagerange
                if not form.pagerange.data == '':
                    options['page-ranges'] = "".join(form.pagerange.data.encode('ascii','ignore').split())
                # options: side
                if form.side.data == None or form.side.data == 'B':
                    options['sides'] = 'two-sided-long-edge'
                else:
                    options['sides'] = 'one-sided'
                # options: number-up
                if not form.numberup.data == 1:
                    options['number-up'] = form.numberup.data


                # connect and print

                conn = cups.Connection()
                conn.printFile(form.printer.data, os.path.join(UPLOAD_FOLDER, filename), form.printer.data + '_' + filename , options)



        return render_template('sb-admin/pages/forms.html', admin_view=self, form=form)         
        
    @expose('/ui/panelswells')
    def panelswells(self):        
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
            
        self._stubs()    
        self.header = "Panels Wells"
        return render_template('sb-admin/pages/ui/panels-wells.html', admin_view=self)
        
    @expose('/ui/buttons')
    def buttons(self):        
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
            
        self._stubs()    
        self.header = "Buttons"
        return render_template('sb-admin/pages/ui/buttons.html', admin_view=self) 
                                
    @expose('/ui/notifications')
    def notifications(self):        
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
            
        self._stubs()    
        self.header = "Notifications"
        return render_template('sb-admin/pages/ui/notifications.html', admin_view=self)                         

    @expose('/ui/typography')
    def typography(self):        
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
            
        self._stubs()    
        self.header = "Typography"
        return render_template('sb-admin/pages/ui/typography.html', admin_view=self)
        
    @expose('/ui/icons')
    def icons(self):        
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
            
        self._stubs()    
        self.header = "Icons"
        return render_template('sb-admin/pages/ui/icons.html', admin_view=self)         
        
    @expose('/ui/grid')
    def grid(self):        
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
            
        self._stubs()    
        self.header = "Grid"
        return render_template('sb-admin/pages/ui/grid.html', admin_view=self)         

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return render_template('sb-admin/pages/login.html', form=form)

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))
        
class BlankView(admin.BaseView):
    @expose('/')
    def index(self):
        return render_template('sb-admin/pages/blank.html', admin_view=self)
