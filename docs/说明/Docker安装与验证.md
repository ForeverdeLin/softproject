# Docker安装与验证指南

## 一、安装Docker Desktop（Windows）

### 1.1 下载Docker Desktop

1. 访问官网：https://www.docker.com/products/docker-desktop/
2. 下载 **Docker Desktop for Windows**
3. 运行安装程序

### 1.2 安装要求

- **Windows 10 64位**：专业版、企业版或教育版（版本1903或更高）
- **启用WSL 2**：Docker Desktop会自动提示安装
- **虚拟化支持**：确保BIOS中启用了虚拟化

### 1.3 安装步骤

1. 运行安装程序
2. 按照提示完成安装
3. **重启电脑**（必须）
4. 启动Docker Desktop

---

## 二、验证Docker是否安装成功

### 2.1 检查Docker版本

打开PowerShell或命令提示符，运行：

```powershell
docker --version
```

**预期输出：**
```
Docker version 24.0.0, build xxxxxx
```

### 2.2 检查Docker Compose版本

```powershell
docker-compose --version
```

**预期输出：**
```
Docker Compose version v2.20.0
```

### 2.3 检查Docker是否运行

```powershell
docker info
```

**如果Docker正在运行，会显示：**
```
Client:
 Version:    24.0.0
 ...

Server:
 Containers: 0
 Running: 0
 ...
```

**如果Docker未运行，会显示错误：**
```
error during connect: ...
```

**解决方法：** 启动Docker Desktop应用程序

---

## 三、测试Docker基本功能

### 3.1 运行Hello World测试

```powershell
docker run hello-world
```

**预期输出：**
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

### 3.2 查看Docker镜像

```powershell
docker images
```

---

## 四、验证项目Docker配置

### 4.1 检查Docker文件是否存在

在项目目录下检查：

```powershell
# 检查文件
ls Dockerfile
ls docker-compose.yml
```

### 4.2 测试构建Docker镜像

```powershell
# 在项目根目录下
docker-compose build
```

**预期输出：**
```
[+] Building 15.2s (8/8) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 32B
 ...
 => => writing image sha256:xxxxx
```

### 4.3 测试启动容器

```powershell
docker-compose up -d
```

**预期输出：**
```
[+] Running 2/2
 ✔ Container campus-lost-found-web  Started
```

### 4.4 检查容器状态

```powershell
docker-compose ps
```

**预期输出：**
```
NAME                        STATUS
campus-lost-found-web       Up
```

### 4.5 查看容器日志

```powershell
docker-compose logs
```

**预期输出：**
```
web  |  * Running on http://0.0.0.0:5000
```

### 4.6 测试访问

打开浏览器访问：`http://localhost:5000`

如果能看到系统首页，说明Docker部署成功！

### 4.7 停止容器

```powershell
docker-compose down
```

---

## 五、常见问题排查

### Q1: `docker: command not found`

**原因：** Docker未安装或未添加到PATH

**解决：**
1. 安装Docker Desktop
2. 重启电脑
3. 确保Docker Desktop正在运行

### Q2: `Cannot connect to the Docker daemon`

**原因：** Docker Desktop未启动

**解决：**
1. 打开Docker Desktop应用程序
2. 等待Docker启动完成（右下角图标变绿）
3. 重新运行命令

### Q3: `WSL 2 installation is incomplete`

**原因：** WSL 2未正确安装

**解决：**
1. 按照Docker Desktop提示安装WSL 2
2. 或手动安装：`wsl --install`

### Q4: `Port 5000 is already in use`

**原因：** 5000端口被占用

**解决：**
1. 修改 `docker-compose.yml` 中的端口映射
2. 或关闭占用5000端口的程序

### Q5: `Build failed`

**原因：** 构建过程中出错

**解决：**
1. 查看详细错误信息：`docker-compose build --no-cache`
2. 检查 `Dockerfile` 和 `requirements.txt` 是否正确
3. 确保网络连接正常（需要下载镜像）

---

## 六、快速验证脚本

创建一个验证脚本 `verify_docker.ps1`：

```powershell
# 验证Docker安装
Write-Host "检查Docker版本..." -ForegroundColor Green
docker --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker未安装或未启动" -ForegroundColor Red
    exit 1
}

Write-Host "检查Docker Compose版本..." -ForegroundColor Green
docker-compose --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker Compose未安装" -ForegroundColor Red
    exit 1
}

Write-Host "检查Docker运行状态..." -ForegroundColor Green
docker info | Select-String "Server Version"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker未运行，请启动Docker Desktop" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker环境正常！" -ForegroundColor Green
```

运行验证脚本：
```powershell
.\verify_docker.ps1
```

---

## 七、验证清单

完成以下检查，确保Docker可用：

- [ ] Docker Desktop已安装
- [ ] Docker Desktop正在运行（系统托盘图标为绿色）
- [ ] `docker --version` 命令成功
- [ ] `docker-compose --version` 命令成功
- [ ] `docker info` 命令成功
- [ ] `docker run hello-world` 测试成功
- [ ] `docker-compose build` 构建成功
- [ ] `docker-compose up` 启动成功
- [ ] 浏览器能访问 `http://localhost:5000`

---

**如果所有检查都通过，说明Docker环境配置成功！** ✅

