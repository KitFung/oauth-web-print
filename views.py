import flask_login as login
import flask_admin as admin
from flask_admin import helpers, expose
from flask_oauthlib.client import OAuth, OAuthException
from flask import redirect, url_for, request, render_template, session

## temp
from user import User

from loginform import LoginForm
from facebook import facebook
import stub as stub

                       
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
        
    @expose('/forms')
    def forms(self):        
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
            
        self._stubs()    
        self.header = "Forms"
        return render_template('sb-admin/pages/forms.html', admin_view=self)         
        
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
        callback = url_for(
            '.facebook_authorized',
            next=request.args.get('next') or request.referrer or None,
            _external=True
        )
        return facebook.authorize(callback=callback)

    @expose('/login/authorized')
    def facebook_authorized(self):
        resp = facebook.authorized_response()
        if resp is None:
            return 'Access denied: reason=%s error=%s' % (
                request.args['error_reason'],
                request.args['error_description']
            )
        if isinstance(resp, OAuthException):
            return 'Access denied: %s' % resp.message

        session['oauth_token'] = (resp['access_token'], '')
        me = facebook.get('/me')

        print("================== %s" % me.data['id'])
        user = User.get(me.data['id'])
        if user is None:
            return 'Logged in as id=%s name=%s redirect=%s, Please add your id to database' % \
                (me.data['id'], me.data['name'], request.args.get('next'))
        else:
            login.login_user(user)

        return redirect(url_for('.index'))


    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))
        
class BlankView(admin.BaseView):
    @expose('/')
    def index(self):
        return render_template('sb-admin/pages/blank.html', admin_view=self)
