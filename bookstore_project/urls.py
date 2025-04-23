from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store.views import BookListView # Import a default view for the homepage

urlpatterns = [
    # Homepage - Pointing to the book list view for simplicity
    path('', BookListView.as_view(), name='home'),
    # App URLs
    path('accounts/', include('accounts.urls')),
    path('store/', include('store.urls')),
    path('custom-admin/', include('admin_panel.urls')), # Keep this for your custom admin
    # NO MORE: path('admin/', admin.site.urls),
]

# Serve static files during development (keep this part)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])