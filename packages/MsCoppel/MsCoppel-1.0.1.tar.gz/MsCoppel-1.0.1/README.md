# MsCoppel

Paquete para implmentar microservicios basados en mensajes, utilizando la cola de mensaje de kafka

```python

from MsCoppel import microservices, Manager, Options

@Manager.Define(Options(
    App: ,
    Debug: ,
    Kafka: ,
    Name: ,
    Public: ,
    Type: ,
    Version: 
))
class Demo(microservices):

    @MsManager.Errors
    def misErrores(self):
        return {'-12', 'Mensaje'}

    @MsManager.List
    def listar():
        pass

    @MsManager.Get
    def info():
        pass
    
    @MsManager.Create
    def nuevo():
        pass
    
    @MsManager.Update
    def actualizar():
        pass

    @MsManager.Delete
    def eliminar():
        pass
    
    @MsManager.Listener
    def general():
        pass

```