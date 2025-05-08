from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.models import LogEntry
from .models import CustomUser, Product
import json

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class CustomLoginView(LoginView):
    template_name = 'admin_app/login.html'
    
    def dispatch(self, request, *args, **kwargs):
        """Redirect to dashboard if user is already logged in"""
        if request.user.is_authenticated:
            return redirect('admin_app:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return '/api/dashboard/'  # Updated to match our URL pattern
    
    def form_valid(self, form):
        """Handle successful form submission"""
        login(self.request, form.get_user())
        messages.success(self.request, 'Login successful!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Handle invalid form submission"""
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)
    
    def post(self, request, *args, **kwargs):
        # Check if the request is an API request
        if request.headers.get('Content-Type') == 'application/json':
            try:
                data = json.loads(request.body)
                username = data.get('username')
                password = data.get('password')
                
                if not username or not password:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Please provide both username and password'
                    }, status=400)
                
                user = authenticate(request, username=username, password=password)
                
                if user is not None:
                    login(request, user)
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Login successful',
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'is_staff': user.is_staff,
                            'is_verified': user.is_verified if hasattr(user, 'is_verified') else False
                        }
                    })
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Invalid username or password'
                    }, status=401)
                    
            except json.JSONDecodeError:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid JSON data'
                }, status=400)
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                }, status=500)
        
        # Handle regular form submission
        return super().post(request, *args, **kwargs)

@login_required
def dashboard(request):
    """Dashboard view showing statistics and recent activity"""
    context = {
        'total_users': CustomUser.objects.count(),
        'total_products': Product.objects.count(),
        'verified_users': CustomUser.objects.filter(is_verified=True).count(),
        'recent_logs': LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:5]
    }
    return render(request, 'admin_app/index.html', context)

def logout_view(request):
    """Custom logout view that redirects to login page"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('admin_app:login')
