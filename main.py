from website import create_app
import flask_monitoringdashboard as dashboard
import dash_html_components as html

app = create_app()
dashboard.bind(app)

if __name__ == '__main__':
    app.run(debug=True)
    
    
