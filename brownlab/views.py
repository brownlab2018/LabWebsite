from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import FileUpload, FileData
from .forms import FileUploadForm

# Create your views here.
def home(request):
	featured_image = FileData.objects.order_by('?')[0]

	context = {
		'featured_image': featured_image
	}
	
	return render(request, 'brownlab/home.html', context)


def the_lab(request):
	title = 'The Lab'

	context = {
		'title': title
	}

	return render(request, 'brownlab/the_lab.html', context)


def instruments(request):
	title = 'Our Instruments'

	context = {
		'title': title
	}

	return render(request, 'brownlab/instruments.html', context)


def browse(request):
	title = 'Browse Datasets'

	total_count = FileData.objects.count()

	newest_data = FileData.objects.latest('acq_date')

	datasets = FileData.objects.all().order_by('-acq_date')

	paginator = Paginator(datasets, 30)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'title': title,
		'total_count': total_count,
		'newest_data': newest_data,
		'datasets': datasets,
		'page_obj': page_obj
	}

	return render(request, 'brownlab/browse.html', context)


def browse_detail(request, id):
	title = 'Detail View'

	obj = get_object_or_404(FileData, id=id)

	context = {
		'title': title,
		'object': obj
	}

	return render(request, 'brownlab/browse_detail.html', context)


def is_valid_queryparam(param):
	return param != '' and param is not None


def search(request):
	title = 'Search Datasets'

	qs = FileData.objects.all().order_by('-acq_date')

	acq_date_start_query = request.GET.get('acq_date_start')
	acq_date_end_query = request.GET.get('acq_date_end')

	scan_size_min_query = request.GET.get('scan_size_min')
	scan_size_max_query = request.GET.get('scan_size_max')

	setpoint_min_query = request.GET.get('setpoint_min')
	setpoint_max_query = request.GET.get('setpoint_max')

	bias_min_query = request.GET.get('bias_min')
	bias_max_query = request.GET.get('bias_max')

	comment_query = request.GET.get('comment')

	if is_valid_queryparam(acq_date_start_query):
		qs = qs.filter(acq_date__lte=acq_date_start_query)

	if is_valid_queryparam(acq_date_end_query):
		qs = qs.filter(acq_date__gte=acq_date_end_query)

	if is_valid_queryparam(scan_size_min_query):
		qs = qs.filter(xysize_nm__gte=scan_size_min_query)

	if is_valid_queryparam(scan_size_max_query):
		qs = qs.filter(xysize_nm__lte=scan_size_max_query)

	if is_valid_queryparam(setpoint_min_query):
		qs = qs.filter(setpoint__gte=setpoint_min_query)

	if is_valid_queryparam(setpoint_max_query):
		qs = qs.filter(setpoint__lte=setpoint_max_query)

	if is_valid_queryparam(bias_min_query):
		qs = qs.filter(bias__gte=bias_min_query)

	if is_valid_queryparam(bias_max_query):
		qs = qs.filter(bias__lte=bias_max_query)

	if is_valid_queryparam(comment_query):
		qs = qs.filter(comment__icontains=comment_query)

	total_count = FileData.objects.count()
	search_results_count = qs.count()

	paginator = Paginator(qs, 30)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'title': title,
		'qs': qs,
		'total_count': total_count,
		'search_results_count': search_results_count,
		'page_obj': page_obj
	}

	return render(request, 'brownlab/search.html', context)



@login_required(login_url='login')
def upload(request):
	title = 'Upload Files'

	if request.method == 'POST':
		form = FileUploadForm(request.POST, request.FILES)

		sm4 = request.FILES

		if form.is_valid():
			FileUpload = form.save(commit=False)
			FileUpload.author = request.user
			FileUpload = FileUpload.save()
			return redirect('upload')

	else:
		form = FileUploadForm()

	context = {
		'title': title,
		'form': form
	}

	return render(request, 'brownlab/upload.html', context)


@login_required(login_url='login')
def uploadpage(request):
	if request.method == 'GET':
		title = 'Upload Datasets'

		uploaded_files = FileUpload.objects.all()
		recent_files = FileUpload.objects.all().order_by('-date_uploaded')[:10]

		context = {
			'title': title,
			'uploaded_files': uploaded_files,
			'recent_files': recent_files
		}

		return render(request, 'brownlab/new_upload.html', context)

	if request.method == 'POST':
		form = FileUploadForm(request.POST, request.FILES)

		if form.is_valid():
			file_uploaded = form.save()

			data = {
				'is_valid': True,
				'name': file_uploaded.file.name,
				'url': file_uploaded.file.url
			}

		else:
			data = {
				'is_valid': False
			}

		return JsonResponse(data)


def cleardatabase(request):
	for dataset in FileUpload.objects.all():
		dataset.file.delete()
		dataset.delete()

	return redirect(request.POST.get('next'))


def loginpage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username AND/OR Password is Incorrect')

	context = {}

	return render(request, 'brownlab/login.html', context)


def logoutpage(request):
	logout(request)

	return redirect('home')
