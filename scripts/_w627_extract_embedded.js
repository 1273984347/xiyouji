// W627：从两 EN 页提取 EMBEDDED 对象（Node 原生 JS 解析·零正则 hack），落盘为 JSON 供生成器消费。
// 用法：node scripts/_w627_extract_embedded.js
const fs = require("fs");
const path = require("path");

function extract(htmlPath) {
    const s = fs.readFileSync(htmlPath, "utf8");
    const marker = "const EMBEDDED = ";
    const start = s.indexOf(marker);
    if (start < 0) throw new Error("EMBEDDED not found in " + htmlPath);
    // 顶层闭合：EMBEDDED 后第一个「\n    };」（4 空格缩进顶层；嵌套层缩进更深）
    const end = s.indexOf("\n    };", start);
    if (end < 0) throw new Error("EMBEDDED terminator not found in " + htmlPath);
    const literal = s.slice(start + marker.length, end + "\n    }".length); // 含结尾 }（不含分号）
    return eval("(" + literal + ")");
}

const root = path.resolve(__dirname, "..");
const out = {
    methodology: extract(path.join(root, "site", "en", "methodology-matrix.html")),
    chart: extract(path.join(root, "site", "en", "chart-design.html")),
};
const dst = path.join(root, "scripts", "output", "_w627_embedded_en.json");
fs.writeFileSync(dst, JSON.stringify(out, null, 1), "utf8");
console.log("written:", dst);
console.log("methodology keys:", Object.keys(out.methodology).join(","));
console.log("chart keys:", Object.keys(out.chart).join(","));
