from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import User_Image, Result, Counter
from .forms import ImageForm

def home(request):
    images = User_Image.objects
    return render(request, 'choose/home.html', {'images': images})

def allimages(request):
    return home(request)

def image_detail(request, image_id):
    image_detail_ob = get_object_or_404(User_Image, pk=image_id)
    img_name = image_detail_ob.display_data()
    result = get_list_or_404(Result, image=img_name)
    counter = Counter()
    return render(request, 'choose/image.html', {'image_detail':image_detail_ob, 'result': result, 'counter': counter})
def process_form(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            im = form.save()
    else:
        form = ImageForm()
    return render(request, 'choose/upload.html', {'form': form})
