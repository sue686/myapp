// 加载 SheetJS 库
const script = document.createElement("script");
script.src = "https://cdn.sheetjs.com/xlsx-0.20.0/package/dist/xlsx.full.min.js";
script.onload = function () {
    addExportButton(); // 在加载完库后添加导出按钮
};
document.head.appendChild(script);

// Step 1: 定义函数以获取学生信息和表格数据
function getStudentData() {
    const studentID = document.querySelector("#ctl00_Main_sId")?.innerText.trim() || "N/A";
    const studentName = document.querySelector("#ctl00_Main_sName")?.innerText.trim() || "N/A";
    const coursesEnrolled = document.querySelector("#ctl00_Main_dropCourseName option[selected]")?.innerText.trim() || "N/A";

    const table = document.querySelector("#ctl00_Main_gridStuPayment");
    const rows = table?.querySelectorAll("tbody tr") || [];
    const data = [];

    rows.forEach((row) => {
        const cells = row.querySelectorAll("td");
        if (cells.length > 0 && cells[0]?.innerText.trim() !== "") {
            // 提取并格式化日期
            const dueDate = formatDate(cells[2]?.innerText.trim() || "");

            // 提取并计算 Commission 的总值
            const commissionRaw = cells[9]?.innerText.trim() || "";
            const commissionTotal = calculateCommission(commissionRaw);

            data.push({
                "Student ID": studentID,
                "Student Name": studentName,
                "Courses Enrolled": coursesEnrolled,
                "Agent Name": cells[4]?.innerText.trim() || "",
                "Due Date": dueDate,
                "Fees": cells[5]?.innerText.trim() || "",
                "Commission": commissionTotal.toFixed(2), // 保留两位小数
            });
        }
    });

    return data.filter((item) => Object.values(item).some(value => value.trim() !== ""));
}

// 格式化日期函数
function formatDate(dateStr) {
    const months = {
        Jan: "01", Feb: "02", Mar: "03", Apr: "04", May: "05", Jun: "06",
        Jul: "07", Aug: "08", Sep: "09", Oct: "10", Nov: "11", Dec: "12",
    };
    const parts = dateStr.split(" ");
    if (parts.length === 3) {
        const day = parts[0];
        const month = months[parts[1]];
        const year = `20${parts[2]}`; // 假设年份是 2000 后
        return `${day}/${month}/${year}`;
    }
    return dateStr;
}

// 计算 Commission 的总值
function calculateCommission(commissionStr) {
    const matches = commissionStr.match(/([\d]+\.\d{2})/g);
    if (matches && matches.length >= 2) {
        const value1 = parseFloat(matches[0]);
        const value2 = parseFloat(matches[1]);
        return value1 + value2;
    }
    return 0;
}

// Step 2: 定义导出 Excel 的函数
function exportDataToExcel() {
    const data = getStudentData();
    if (data.length === 0) {
        alert("未找到数据，请检查页面内容！");
        return;
    }

    const workbook = XLSX.utils.book_new();
    const worksheet = XLSX.utils.json_to_sheet(data);
    XLSX.utils.book_append_sheet(workbook, worksheet, "Student Data");

    XLSX.writeFile(workbook, "Student_Data.xlsx");
    alert("数据已成功导出！");
}

// Step 3: 添加导出按钮
function addExportButton() {
    const button = document.createElement("button");
    button.innerText = "导出数据到 Excel";
    button.style.backgroundColor = "#4CAF50";
    button.style.color = "white";
    button.style.border = "none";
    button.style.padding = "10px 20px";
    button.style.margin = "10px";
    button.style.cursor = "pointer";
    button.onclick = exportDataToExcel;

    const container = document.querySelector(".content");
    if (container) {
        container.insertBefore(button, container.firstChild);
    }
}
