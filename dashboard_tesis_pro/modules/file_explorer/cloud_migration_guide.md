# Guía de Migración a la Nube - Explorador de Archivos

## 🌐 Introducción

Esta guía detalla los pasos para migrar el módulo de Explorador de Archivos del Dashboard Tesis Pro a diferentes plataformas en la nube, manteniendo la funcionalidad, seguridad y rendimiento.

## 🎯 Opciones de Migración

### 1. AWS (Amazon Web Services)

#### Componentes AWS Recomendados:
- **EC2**: Instancia para FileBrowser
- **S3**: Almacenamiento de archivos
- **RDS**: Base de datos (opcional)
- **CloudFront**: CDN para archivos estáticos
- **IAM**: Gestión de accesos
- **VPC**: Red privada virtual

#### Pasos de Migración:

```bash
# 1. Crear instancia EC2
aws ec2 run-instances \
    --image-id ami-0c02fb55956c7d316 \
    --instance-type t3.micro \
    --key-name dashboard-key \
    --security-group-ids sg-xxxxxxxxx

# 2. Configurar S3 bucket
aws s3 mb s3://dashboard-tesis-pro-files
aws s3api put-bucket-versioning \
    --bucket dashboard-tesis-pro-files \
    --versioning-configuration Status=Enabled

# 3. Configurar IAM role
aws iam create-role \
    --role-name FileBrowserRole \
    --assume-role-policy-document file://trust-policy.json
```

#### Configuración FileBrowser para AWS:
```json
{
  "port": 8058,
  "address": "0.0.0.0",
  "root": "/mnt/s3fs/dashboard-data",
  "database": "/opt/filebrowser/filebrowser.db",
  "auth": {
    "method": "proxy",
    "header": "X-Forwarded-User"
  },
  "branding": {
    "name": "Dashboard Tesis Pro - Cloud",
    "color": "#FF9900"
  }
}
```

### 2. Google Cloud Platform (GCP)

#### Componentes GCP Recomendados:
- **Compute Engine**: VM para FileBrowser
- **Cloud Storage**: Almacenamiento de archivos
- **Cloud SQL**: Base de datos
- **Cloud CDN**: Distribución de contenido
- **Cloud IAM**: Gestión de identidades

#### Script de Despliegue:
```bash
#!/bin/bash
# deploy-gcp.sh

# Crear VM
gcloud compute instances create dashboard-filebrowser \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud \
    --tags=http-server,https-server

# Crear bucket de almacenamiento
gsutil mb gs://dashboard-tesis-pro-data

# Configurar permisos
gsutil iam ch serviceAccount:dashboard-sa@project.iam.gserviceaccount.com:objectAdmin gs://dashboard-tesis-pro-data
```

### 3. Microsoft Azure

#### Componentes Azure Recomendados:
- **Virtual Machines**: VM para FileBrowser
- **Blob Storage**: Almacenamiento de archivos
- **Azure SQL**: Base de datos
- **Azure CDN**: Red de distribución
- **Azure AD**: Autenticación

#### Template ARM:
```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "resources": [
    {
      "type": "Microsoft.Compute/virtualMachines",
      "apiVersion": "2021-03-01",
      "name": "dashboard-vm",
      "location": "[resourceGroup().location]",
      "properties": {
        "hardwareProfile": {
          "vmSize": "Standard_B1s"
        },
        "osProfile": {
          "computerName": "dashboard-vm",
          "adminUsername": "azureuser"
        }
      }
    }
  ]
}
```

### 4. Docker + Kubernetes

#### Dockerfile:
```dockerfile
FROM ubuntu:22.04

# Instalar dependencias
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Instalar FileBrowser
RUN curl -fsSL https://raw.githubusercontent.com/filebrowser/get/master/get.sh | bash

# Copiar configuración
COPY config.json /etc/filebrowser/
COPY custom/ /etc/filebrowser/custom/

# Exponer puerto
EXPOSE 8058

# Comando de inicio
CMD ["filebrowser", "--config", "/etc/filebrowser/config.json"]
```

#### Kubernetes Deployment:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dashboard-filebrowser
spec:
  replicas: 2
  selector:
    matchLabels:
      app: dashboard-filebrowser
  template:
    metadata:
      labels:
        app: dashboard-filebrowser
    spec:
      containers:
      - name: filebrowser
        image: dashboard-tesis-pro/filebrowser:latest
        ports:
        - containerPort: 8058
        volumeMounts:
        - name: data-volume
          mountPath: /data
      volumes:
      - name: data-volume
        persistentVolumeClaim:
          claimName: dashboard-data-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: dashboard-filebrowser-service
spec:
  selector:
    app: dashboard-filebrowser
  ports:
  - port: 80
    targetPort: 8058
  type: LoadBalancer
```

## 🔒 Consideraciones de Seguridad

### 1. Autenticación y Autorización
```python
# oauth_config.py
OAUTH_PROVIDERS = {
    'google': {
        'client_id': 'your-google-client-id',
        'client_secret': 'your-google-client-secret',
        'redirect_uri': 'https://your-domain.com/auth/google/callback'
    },
    'azure': {
        'client_id': 'your-azure-client-id',
        'client_secret': 'your-azure-client-secret',
        'tenant_id': 'your-tenant-id'
    }
}
```

### 2. Cifrado de Datos
```bash
# Configurar cifrado en tránsito
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/dashboard.key \
    -out /etc/ssl/certs/dashboard.crt

# Configurar cifrado en reposo (AWS)
aws s3api put-bucket-encryption \
    --bucket dashboard-tesis-pro-files \
    --server-side-encryption-configuration \
    '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'
```

### 3. Firewall y Redes
```bash
# Configurar firewall (Ubuntu)
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 8058/tcp  # FileBrowser
ufw enable

# Configurar nginx como proxy reverso
server {
    listen 443 ssl;
    server_name dashboard.yourdomain.com;
    
    ssl_certificate /etc/ssl/certs/dashboard.crt;
    ssl_certificate_key /etc/ssl/private/dashboard.key;
    
    location / {
        proxy_pass http://localhost:8058;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📊 Monitoreo y Logging

### 1. Configuración de Logs
```python
# logging_config.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler('/var/log/dashboard/filebrowser.log', 
                              maxBytes=10485760, backupCount=5),
            logging.StreamHandler()
        ]
    )
```

### 2. Métricas de Rendimiento
```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Métricas
file_uploads = Counter('filebrowser_uploads_total', 'Total file uploads')
file_downloads = Counter('filebrowser_downloads_total', 'Total file downloads')
active_users = Gauge('filebrowser_active_users', 'Active users')
request_duration = Histogram('filebrowser_request_duration_seconds', 'Request duration')

def start_metrics_server():
    start_http_server(8061)
```

## 🚀 Scripts de Automatización

### Script de Migración Completa:
```bash
#!/bin/bash
# migrate_to_cloud.sh

set -e

echo "🌐 Iniciando migración a la nube..."

# Variables
CLOUD_PROVIDER=${1:-aws}
DOMAIN=${2:-dashboard.example.com}
REGION=${3:-us-west-2}

# Funciones
migrate_aws() {
    echo "☁️  Migrando a AWS..."
    # Crear infraestructura
    terraform init
    terraform plan -var="domain=$DOMAIN" -var="region=$REGION"
    terraform apply -auto-approve
    
    # Desplegar aplicación
    docker build -t dashboard-filebrowser .
    docker tag dashboard-filebrowser:latest $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/dashboard-filebrowser:latest
    docker push $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/dashboard-filebrowser:latest
}

migrate_gcp() {
    echo "🌩️  Migrando a GCP..."
    gcloud config set project $GCP_PROJECT_ID
    gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/dashboard-filebrowser
    gcloud run deploy dashboard-filebrowser \
        --image gcr.io/$GCP_PROJECT_ID/dashboard-filebrowser \
        --platform managed \
        --region $REGION \
        --allow-unauthenticated
}

migrate_azure() {
    echo "☁️  Migrando a Azure..."
    az group create --name dashboard-rg --location $REGION
    az container create \
        --resource-group dashboard-rg \
        --name dashboard-filebrowser \
        --image dashboard-filebrowser:latest \
        --dns-name-label dashboard-tesis-pro \
        --ports 8058
}

# Ejecutar migración según proveedor
case $CLOUD_PROVIDER in
    aws)
        migrate_aws
        ;;
    gcp)
        migrate_gcp
        ;;
    azure)
        migrate_azure
        ;;
    *)
        echo "❌ Proveedor no soportado: $CLOUD_PROVIDER"
        echo "Proveedores disponibles: aws, gcp, azure"
        exit 1
        ;;
esac

echo "✅ Migración completada!"
echo "🌐 URL de acceso: https://$DOMAIN"
```

## 📋 Checklist de Migración

### Pre-migración
- [ ] Backup completo de datos y configuración
- [ ] Documentar configuración actual
- [ ] Probar en entorno de desarrollo
- [ ] Configurar DNS y certificados SSL
- [ ] Preparar scripts de rollback

### Durante la migración
- [ ] Ejecutar scripts de migración
- [ ] Verificar conectividad
- [ ] Probar autenticación
- [ ] Validar permisos de archivos
- [ ] Confirmar integración con otros módulos

### Post-migración
- [ ] Monitorear logs y métricas
- [ ] Probar funcionalidad completa
- [ ] Actualizar documentación
- [ ] Entrenar usuarios en nuevos accesos
- [ ] Configurar backups automáticos

## 💰 Estimación de Costos

### AWS (mensual)
- EC2 t3.micro: $8.50
- S3 (100GB): $2.30
- CloudFront: $1.00
- **Total estimado: $11.80/mes**

### GCP (mensual)
- Compute Engine e2-micro: $6.11
- Cloud Storage (100GB): $2.00
- Cloud CDN: $0.80
- **Total estimado: $8.91/mes**

### Azure (mensual)
- VM B1s: $7.59
- Blob Storage (100GB): $1.80
- Azure CDN: $0.87
- **Total estimado: $10.26/mes**

## 🔧 Mantenimiento y Actualizaciones

### Script de Actualización:
```bash
#!/bin/bash
# update_cloud_deployment.sh

echo "🔄 Actualizando despliegue en la nube..."

# Backup antes de actualizar
kubectl create backup dashboard-backup-$(date +%Y%m%d-%H%M%S)

# Actualizar imagen
kubectl set image deployment/dashboard-filebrowser \
    filebrowser=dashboard-tesis-pro/filebrowser:latest

# Verificar despliegue
kubectl rollout status deployment/dashboard-filebrowser

echo "✅ Actualización completada!"
```

## 📞 Soporte y Troubleshooting

### Problemas Comunes:

1. **Error de conectividad**
   - Verificar firewall y security groups
   - Confirmar configuración de DNS

2. **Problemas de autenticación**
   - Revisar configuración OAuth
   - Verificar certificados SSL

3. **Rendimiento lento**
   - Optimizar configuración de CDN
   - Escalar recursos de compute

### Contactos de Soporte:
- **AWS**: https://aws.amazon.com/support/
- **GCP**: https://cloud.google.com/support/
- **Azure**: https://azure.microsoft.com/support/

---

*Esta guía se actualiza regularmente. Última revisión: Julio 2024*

