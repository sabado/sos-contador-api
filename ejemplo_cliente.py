"""
Cliente Python para la API de SOS Contador
Ejemplo de implementación con manejo de errores y reintentos
"""

import os
import requests
import time
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class SOSContadorClient:
    """Cliente para interactuar con la API de SOS Contador"""
    
    def __init__(
        self,
        usuario: Optional[str] = None,
        password: Optional[str] = None,
        cuit_id: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        """
        Inicializar cliente de SOS Contador
        
        Args:
            usuario: Email de usuario (o usar SOS_USUARIO de .env)
            password: Contraseña (o usar SOS_PASSWORD de .env)
            cuit_id: ID de CUIT (o usar SOS_CUIT_ID de .env)
            base_url: URL base de la API (opcional)
        """
        self.usuario = usuario or os.getenv('SOS_USUARIO')
        self.password = password or os.getenv('SOS_PASSWORD')
        self.cuit_id = cuit_id or os.getenv('SOS_CUIT_ID')
        self.base_url = base_url or os.getenv(
            'SOS_API_BASE_URL',
            'https://api.sos-contador.com/api-comunidad'
        )
        
        self.user_token: Optional[str] = None
        self.cuit_token: Optional[str] = None
        self.session = requests.Session()
        
        # Validar credenciales
        if not self.usuario or not self.password:
            raise ValueError(
                "Credenciales no configuradas. "
                "Usar parámetros o variables de entorno SOS_USUARIO y SOS_PASSWORD"
            )
    
    def login(self) -> str:
        """
        Realizar login y obtener token de usuario
        
        Returns:
            Token de usuario (JWT)
        """
        url = f"{self.base_url}/login"
        data = {
            "usuario": self.usuario,
            "password": self.password
        }
        
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            
            self.user_token = response.json()["jwt"]
            print("✅ Login exitoso")
            return self.user_token
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error en login: {e}")
    
    def get_cuit_token(self, cuit_id: Optional[str] = None) -> str:
        """
        Obtener token de CUIT
        
        Args:
            cuit_id: ID de CUIT (opcional, usa self.cuit_id si no se provee)
            
        Returns:
            Token de CUIT (JWT)
        """
        if not self.user_token:
            self.login()
        
        cuit_id = cuit_id or self.cuit_id
        if not cuit_id:
            raise ValueError("cuit_id no configurado")
        
        url = f"{self.base_url}/cuit/credentials/{cuit_id}"
        headers = {"Authorization": f"Bearer {self.user_token}"}
        
        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
            
            self.cuit_token = response.json()["jwt"]
            print(f"✅ Token de CUIT obtenido para ID: {cuit_id}")
            return self.cuit_token
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error obteniendo token de CUIT: {e}")
    
    def _ensure_authenticated(self):
        """Asegurar que tenemos token de CUIT válido"""
        if not self.cuit_token:
            if not self.user_token:
                self.login()
            self.get_cuit_token()
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Realizar request con reintentos
        
        Args:
            method: Método HTTP (GET, POST, etc.)
            endpoint: Endpoint (sin base URL)
            params: Query parameters
            data: Body data
            max_retries: Número máximo de reintentos
            
        Returns:
            Response JSON
        """
        self._ensure_authenticated()
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {"Authorization": f"Bearer {self.cuit_token}"}
        
        for attempt in range(max_retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=data
                )
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise Exception(f"Error después de {max_retries} intentos: {e}")
                
                wait_time = 2 ** attempt  # Backoff exponencial
                print(f"⚠️  Intento {attempt + 1} falló, reintentando en {wait_time}s...")
                time.sleep(wait_time)
        
        raise Exception("No se pudo completar el request")
    
    def listar_clientes(
        self,
        proveedor: bool = True,
        cliente: bool = True,
        registros: int = 16,
        pagina: int = 1
    ) -> Dict[str, Any]:
        """
        Listar clientes y/o proveedores
        
        Args:
            proveedor: Incluir proveedores
            cliente: Incluir clientes
            registros: Registros por página
            pagina: Número de página
            
        Returns:
            Diccionario con clientes/proveedores
        """
        params = {
            "proveedor": str(proveedor).lower(),
            "cliente": str(cliente).lower(),
            "registros": registros,
            "pagina": pagina
        }
        
        return self._request("GET", "/cliente/listado", params=params)


# Ejemplo de uso
if __name__ == "__main__":
    # Crear cliente
    client = SOSContadorClient()
    
    # Login automático al hacer la primera request
    clientes = client.listar_clientes(
        cliente=True,
        proveedor=False,
        registros=10,
        pagina=1
    )
    
    print(f"\n📋 Total de clientes: {clientes.get('total', 'N/A')}")
    print(f"📄 Página: {clientes.get('pagina', 'N/A')}")
    
    # Imprimir primeros clientes
    if 'clientes' in clientes:
        for i, cliente in enumerate(clientes['clientes'][:5], 1):
            print(f"\n{i}. {cliente.get('nombre', 'Sin nombre')}")
            print(f"   CUIT: {cliente.get('cuit', 'N/A')}")
