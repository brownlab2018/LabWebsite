from django.urls import path

from .views import *

urlpatterns = [
	path('', home, name='home'),
	path('about/the-lab/', the_lab, name='the-lab'),
	path('about/instruments/', instruments, name='instruments'),
	path('datasets/browse/', browse, name='browse'),
	path('datasets/browse/<int:id>/', browse_detail, name='browse-detail'),
	path('datasets/search/', search, name='search'),
	# path('upload/', upload, name='upload'),
	path('upload/', uploadpage, name='upload'),
	path('login/', loginpage, name='login'),
	path('logout/', logoutpage, name='logout'),
]