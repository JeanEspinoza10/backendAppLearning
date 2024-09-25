
class Response:
    
    def code200(message, data=[]):
        return{
            "message": message,
            "code": 200,
            "data": data,
        }, 200
    
    def code404(message, data=[]):
        return {
                "message": message,
                "code": 404,
                "data": data,
            },404
    
    def code500(message, data=[]):
        return {
                "message": message,
                "code": 500,
                "data": data,
        },500