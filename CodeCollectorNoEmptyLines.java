package SoftwareCopyright;

import java.io.*;
import java.nio.file.*;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.*;

public class CodeCollectorNoEmptyLines {

    // ========== 配置文件 ==========
    private static final List<SourceConfig> CONFIG_LIST = Arrays.asList(
            // 格式：new SourceConfig("项目名称", "源文件夹路径", "输出文件路径", "文件后缀列表")
            new SourceConfig("Java后端项目",
                    "E:\\code\\19222-【吉林工商】智慧实验室管理平台二期\\jlgs_zhsyseq_v211_ua_ruoyi_cloud_business\\chenrise-modules\\chenrise-device",
                    "E:\\code\\代码提取工具\\java_code.txt",
                    Arrays.asList(".java")),

//            new SourceConfig("Unity项目",
//                    "D:\\Project Code\\047_dbsf_nygl\\chenrise-nenu-u3d\\Assets\\Scripts\\Control",
//                    "C:\\Users\\cloud\\Desktop\\unity_code.txt",
//                    Arrays.asList(".cs")),

            new SourceConfig("前端项目",
                    "E:\\code\\19222-【吉林工商】智慧实验室管理平台二期\\jlgs_zhsyseq_v211_ua_ruoyi_vue_business",
                    "E:\\code\\代码提取工具\\vue_code.txt",
                    Arrays.asList(".vue"))
            // 可以继续添加更多配置...
    );
    // =============================

    public static void main(String[] args) {
        System.out.println("=== 多项目代码收集工具（去除空行版）===");
        System.out.println();

        // 显示配置信息
        displayConfigInfo();

        // 检查所有配置的路径
        if (!checkAllPaths()) {
            waitForExit();
            return;
        }

        // 处理所有配置
        processAllConfigs();

        waitForExit();
    }

    private static void displayConfigInfo() {
        System.out.println("当前配置了 " + CONFIG_LIST.size() + " 个项目：");
        for (int i = 0; i < CONFIG_LIST.size(); i++) {
            SourceConfig config = CONFIG_LIST.get(i);
            System.out.println((i + 1) + ". " + config.projectName);
            System.out.println("   源路径: " + config.sourcePath);
            System.out.println("   输出文件: " + config.outputPath);
            System.out.println("   文件类型: " + config.extensions);
        }
        System.out.println();
    }

    private static boolean checkAllPaths() {
        boolean allValid = true;

        for (SourceConfig config : CONFIG_LIST) {
            File sourceDir = new File(config.sourcePath);
            if (!sourceDir.exists() || !sourceDir.isDirectory()) {
                System.out.println("错误：源路径不存在 - " + config.sourcePath);
                allValid = false;
                continue;
            }

            // 检查输出文件目录
            File outputFile = new File(config.outputPath);
            File parentDir = outputFile.getParentFile();
            if (parentDir != null && !parentDir.exists()) {
                if (!parentDir.mkdirs()) {
                    System.out.println("错误：无法创建输出目录 - " + parentDir.getAbsolutePath());
                    allValid = false;
                }
            }
        }

        return allValid;
    }

    private static void processAllConfigs() {
        int totalProjects = CONFIG_LIST.size();
        int successCount = 0;

        for (int i = 0; i < CONFIG_LIST.size(); i++) {
            SourceConfig config = CONFIG_LIST.get(i);
            System.out.println("================================================");
            System.out.println("正在处理项目 " + (i + 1) + "/" + totalProjects + ": " + config.projectName);
            System.out.println("源路径: " + config.sourcePath);
            System.out.println("输出文件: " + config.outputPath);
            System.out.println("文件类型: " + config.extensions);
            System.out.println();

            if (processSingleConfig(config)) {
                successCount++;
                System.out.println("处理完成: " + config.projectName);
            } else {
                System.out.println("处理失败: " + config.projectName);
            }
            System.out.println();
        }

        System.out.println("================================================");
        System.out.println("总体完成情况: " + successCount + "/" + totalProjects + " 个项目处理成功");

        if (successCount > 0) {
            System.out.println("输出文件列表:");
            for (SourceConfig config : CONFIG_LIST) {
                File outputFile = new File(config.outputPath);
                if (outputFile.exists()) {
                    System.out.println("  " + config.outputPath);
                }
            }
        }
    }

    private static boolean processSingleConfig(SourceConfig config) {
        List<Path> codeFiles = new ArrayList<>();

        // 查找所有匹配的文件
        if (!findCodeFiles(config, codeFiles)) {
            return false;
        }

        if (codeFiles.isEmpty()) {
            System.out.println("警告：未找到匹配的代码文件");
            return true;
        }

        // 处理文件
        return processFiles(config, codeFiles);
    }

    private static boolean findCodeFiles(SourceConfig config, List<Path> codeFiles) {
        Path startPath = Paths.get(config.sourcePath);
        try {
            Files.walkFileTree(startPath, new SimpleFileVisitor<Path>() {
                @Override
                public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) {
                    String fileName = file.toString().toLowerCase();
                    for (String ext : config.extensions) {
                        if (fileName.endsWith(ext.toLowerCase())) {
                            codeFiles.add(file);
                            break;
                        }
                    }
                    return FileVisitResult.CONTINUE;
                }

                @Override
                public FileVisitResult visitFileFailed(Path file, IOException exc) {
                    System.out.println("警告：无法访问文件 - " + file);
                    return FileVisitResult.CONTINUE;
                }
            });
        } catch (IOException e) {
            System.out.println("错误：遍历文件夹时出错 - " + e.getMessage());
            return false;
        }

        System.out.println("找到 " + codeFiles.size() + " 个代码文件");
        return true;
    }

    private static boolean processFiles(SourceConfig config, List<Path> codeFiles) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(config.outputPath, false))) {

//            // 写入文件头信息
//            writer.write("// =================================================");
//            writer.newLine();
//            writer.write("// 项目名称: " + config.projectName);
//            writer.newLine();
//            writer.write("// 源路径: " + config.sourcePath);
//            writer.newLine();
//            writer.write("// 文件类型: " + config.extensions);
//            writer.newLine();
//            writer.write("// 生成时间: " + new Date());
//            writer.newLine();
//            writer.write("// 文件数量: " + codeFiles.size());
//            writer.newLine();
//            writer.write("// =================================================");
//            writer.newLine();

            for (int i = 0; i < codeFiles.size(); i++) {
                Path codeFile = codeFiles.get(i);
                double progress = (double) (i + 1) / codeFiles.size() * 100;

                System.out.println("处理文件 (" + (i + 1) + "/" + codeFiles.size() + ") [" + String.format("%.1f", progress) + "%]: " + codeFile.getFileName());

//                // 写入文件头
//                writer.write("// =================================================");
//                writer.newLine();
//                writer.write("// 文件路径: " + codeFile.toAbsolutePath());
//                writer.newLine();
//                writer.write("// 文件大小: " + formatFileSize(Files.size(codeFile)));
//                writer.newLine();
//                writer.write("// =================================================");
//                writer.newLine();

                // 写入文件内容（去除空行）
                try {
                    List<String> lines = Files.readAllLines(codeFile);
                    boolean lastLineWasEmpty = false;

                    for (String line : lines) {
                        // 去除行首尾的空白字符
                        String trimmedLine = line.trim();

                        // 如果是空行，跳过
                        if (trimmedLine.isEmpty()) {
                            lastLineWasEmpty = true;
                            continue;
                        }

                        // 写入非空行
                        writer.write(line);
                        writer.newLine();
                        lastLineWasEmpty = false;
                    }

                } catch (IOException e) {
                    System.out.println("警告：无法读取文件 - " + codeFile);
//                    writer.write("// 注意：此文件内容无法读取");
//                    writer.newLine();
                }

                // 文件之间不加空行分隔（软著要求）
            }

            writer.flush();
            return true;

        } catch (IOException e) {
            System.out.println("错误：写入输出文件时出错 - " + e.getMessage());
            return false;
        }
    }

    private static String formatFileSize(long size) {
        if (size < 1024) {
            return size + " B";
        } else if (size < 1024 * 1024) {
            return String.format("%.1f KB", size / 1024.0);
        } else {
            return String.format("%.1f MB", size / (1024.0 * 1024.0));
        }
    }

    private static void waitForExit() {
//        System.out.println("按任意键退出...");
//        try {
//            System.in.read();
//        } catch (IOException e) {
//        }
    }

    // 配置类
    static class SourceConfig {
        String projectName;
        String sourcePath;
        String outputPath;
        List<String> extensions;

        SourceConfig(String projectName, String sourcePath, String outputPath, List<String> extensions) {
            this.projectName = projectName;
            this.sourcePath = sourcePath;
            this.outputPath = outputPath;
            this.extensions = extensions;
        }
    }
}
