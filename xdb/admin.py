"""
 XSS Test Driver : cross browser XSS Vector Testing Tool
    Copyright (C) 2012  Erwan ABGRALL

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from xssdb.xdb.models import *
from django.contrib import admin

admin.site.register(Vector)

admin.site.register(Browser)

admin.site.register(Suite)

admin.site.register(Test)

admin.site.register(WebContext)

admin.site.register(BrowserFamily)

admin.site.register(BrowserPlugin)

admin.site.register(Encoding)

admin.site.register(VectorFamily)

