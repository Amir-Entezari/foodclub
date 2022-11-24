
from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('foods', views.FoodViewSet, basename='foods')
router.register('category', views.CategoryViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('Orders', views.OrderViewSet,basename='orders')

foods_router = routers.NestedDefaultRouter(router, 'foods', lookup='food')
foods_router.register('reviews', views.ReviewViewSet, basename='food-reviews')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('cartitem_set', views.CartItemViewSet,
                      basename='cart-cartitems')

urlpatterns = router.urls+foods_router.urls+carts_router.urls

# urlpatterns = [
#     path('',include(router.urls))
# ]
