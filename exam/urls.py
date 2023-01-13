from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from account import views as acc_view
from news import views as news_view

acc_router = DefaultRouter()
acc_router.register('register', acc_view.ProfileRegisterAPIView)

posts_router = DefaultRouter()
posts_router.register('news', news_view.NewsViewSet)
posts_router.register('statuses', news_view.StatusViewSet)


schema_view = get_schema_view(
   openapi.Info(
      title="News API",
      default_version='v-0.01',
      description="API для взаимодействия с новостями API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="myrza-96g@mail.ru"),
      license=openapi.License(name="No License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    # path('', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),
    path('api/account/token/', obtain_auth_token),


    path('api/account/', include(acc_router.urls)),

    path('api/', include(posts_router.urls)),
    path('api/news/<int:news_id>/comment/', news_view.CommentListCreateAPIView.as_view()),
    path('api/news/<int:news_id>/comment/<int:pk>/', news_view.CommentRetrieveUpdateDestroy.as_view()),

    path('api/news/<int:news_id>/<slug:slug>/', news_view.status_news),
    path('api/news/<int:news_id>/comment/<int:comment_id>/<slug:slug>/', news_view.status_comment),
    # documentation URL
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_doc'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc_doc'),


]


