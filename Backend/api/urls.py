
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .views import home
from api.product.urls import urlpatterns as product_urls
from api.payment.urls import urlpatterns as payment_urls
# from api.syllabus.urls import urlpatterns as syllabus_urls
urlpatterns = [
    path('', home),
    path('/product/' , include(product_urls)),
    path('/payment/' , include(payment_urls)),
    # path('/syllabus/' , include(syllabus_urls)),
]

