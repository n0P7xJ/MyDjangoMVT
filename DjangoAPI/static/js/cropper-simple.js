// Простий та надійний Cropper.js для Django
document.addEventListener('DOMContentLoaded', function() {
    let cropper = null;
    let selectedFile = null;
    
    // Знаходимо елементи
    const photoInput = document.getElementById('photo-input') || document.querySelector('input[name="photo"]');
    const cropperContainer = document.getElementById('cropper-container');
    const imagePreview = document.getElementById('image-preview');
    const croppedPreview = document.getElementById('cropped-preview');
    const cropBtn = document.getElementById('crop-btn');
    const resetBtn = document.getElementById('reset-btn');
    
    console.log('Initializing Cropper.js...');
    
    // Перевірка елементів
    if (!photoInput) {
        console.error('Photo input not found!');
        return;
    }
    
    // Обробник вибору файлу
    photoInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file && file.type.startsWith('image/')) {
            selectedFile = file;
            
            if (cropperContainer) {
                cropperContainer.style.display = 'block';
            }
            
            const reader = new FileReader();
            reader.onload = function(event) {
                const img = document.createElement('img');
                img.src = event.target.result;
                img.id = 'crop-image';
                
                if (imagePreview) {
                    imagePreview.innerHTML = '';
                    imagePreview.appendChild(img);
                }
                
                img.onload = function() {
                    cropper = new Cropper(img, {
                        aspectRatio: 1,
                        viewMode: 1,
                        autoCropArea: 0.8,
                        dragMode: 'crop'
                    });
                    
                    if (cropBtn) cropBtn.disabled = false;
                    if (resetBtn) resetBtn.disabled = false;
                };
            };
            reader.readAsDataURL(file);
        }
    });
    
    // Обробник кнопки обрізання
    if (cropBtn) {
        cropBtn.addEventListener('click', function() {
            if (cropper) {
                const canvas = cropper.getCroppedCanvas({
                    width: 200,
                    height: 200
                });
                
                canvas.toBlob(function(blob) {
                    const file = new File([blob], 'cropped.jpg', { type: 'image/jpeg' });
                    const dt = new DataTransfer();
                    dt.items.add(file);
                    photoInput.files = dt.files;
                    
                    if (croppedPreview) {
                        croppedPreview.innerHTML = `<img src="${canvas.toDataURL()}" style="width: 100px; height: 100px; border-radius: 50%; object-fit: cover;">`;
                    }
                });
            }
        });
    }
    
    // Обробник кнопки скидання
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            if (cropper) {
                cropper.destroy();
                cropper = null;
            }
            
            photoInput.value = '';
            if (cropperContainer) {
                cropperContainer.style.display = 'none';
            }
            
            if (cropBtn) cropBtn.disabled = true;
            if (resetBtn) resetBtn.disabled = true;
        });
    }
});
