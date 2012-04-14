from cartoon_app import app
import os
app.run(host='0.0.0.0', port=int(os.environ['PORT']))
