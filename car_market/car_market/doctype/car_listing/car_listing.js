frappe.ui.form.on('Car Listing', {
    refresh: function(frm) {
        // Зургуудыг харуулах функцыг дуудах
        render_image_preview(frm);
    },
    main_image: function(frm) {
        render_image_preview(frm);
    }
});

// Зургийг форматлаж харуулах туслах функц
function render_image_preview(frm) {
    let html_content = `
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #d1d8dd;">
            <div style="display: flex; flex-wrap: wrap; gap: 15px; align-items: flex-start;">
    `;

    // 1. Үндсэн зургийг нэмэх
    if (frm.doc.main_image) {
        html_content += `
            <div style="text-align: center;">
                <p style="font-weight: bold; margin-bottom: 5px; color: #555;">Үндсэн зураг</p>
                <img src="${frm.doc.main_image}" 
                     style="max-width: 250px; height: auto; border-radius: 5px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); cursor: pointer;"
                     onclick="window.open('${frm.doc.main_image}', '_blank')">
            </div>
        `;
    }

    // 2. Галерейн зургуудыг нэмэх
    if (frm.doc.gallery && frm.doc.gallery.length > 0) {
        frm.doc.gallery.forEach((row, index) => {
            if (row.image) {
                html_content += `
                    <div style="text-align: center;">
                        <p style="font-weight: bold; margin-bottom: 5px; color: #555;">Зураг ${index + 1}</p>
                        <img src="${row.image}" 
                             style="max-width: 180px; height: auto; border-radius: 5px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); cursor: pointer;"
                             onclick="window.open('${row.image}', '_blank')">
                    </div>
                `;
            }
        });
    }

    // Хэрэв зураг огт байхгүй бол
    if (!frm.doc.main_image && (!frm.doc.gallery || frm.doc.gallery.length === 0)) {
        html_content += `<p style="color: #888; font-style: italic;">Одоогоор зураг байхгүй байна.</p>`;
    }

    html_content += `
            </div>
        </div>
    `;

    // HTML талбарт агуулгыг оноох
    frm.get_field('image_preview').$wrapper.html(html_content);
}