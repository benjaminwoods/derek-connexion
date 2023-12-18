import sys
sys.path.append('../')
sys.path.append('../src')

# This is required for Vercel
from a2wsgi import ASGIMiddleware
from run import app as asgi_app
app = ASGIMiddleware(asgi_app)
