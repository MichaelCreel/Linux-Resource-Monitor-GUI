#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <limits.h>
#include <string.h>

int main() {
    //CPU INFORMATION
    printf("\n<--- CPU INFORMATION --->\n");
    unsigned long long user1, nice1, system1, idle1;
    unsigned long long user2, nice2, system2, idle2;

    FILE *fp = fopen("/proc/stat", "r");
    fscanf(fp, "cpu %llu %llu %llu %llu", &user1, &nice1, &system1, &idle1);
    fclose(fp);
    usleep(100000); // 100ms sleep

    fp = fopen("/proc/stat", "r");
    fscanf(fp, "cpu %llu %llu %llu %llu", &user2, &nice2, &system2, &idle2);
    fclose(fp);

    unsigned long long total1 = user1 + nice1 + system1 + idle1;
    unsigned long long total2 = user2 + nice2 + system2 + idle2;
    unsigned long long total_diff = total2 - total1;
    unsigned long long idle_diff = idle2 - idle1;
    float cpu_usage = 100.0 * (total_diff - idle_diff) / total_diff;
    printf("CPU Usage: %.2f%%\n", cpu_usage);

    //MEMORY INFORMATION
    FILE *mem = fopen("/proc/meminfo", "r");
    if (mem) {
        printf("\n<--- MEMORY INFORMATION --->\n");

        unsigned long mem_total = 0;
        unsigned long mem_free = 0;
        char label[64];
        unsigned long value;

        while (fscanf(mem, "%63s %lu kB\n", label, &value) == 2) {
            if (strcmp(label, "MemTotal:") == 0) {
                mem_total = value;
            } else if (strcmp(label, "MemAvailable:") == 0) {
                mem_free = value;
            }
            if (mem_total && mem_free) {
                break;
            }
        }
        fclose(mem);

        float mem_total_gb = mem_total / 1024.0 / 1024.0;
        float mem_free_gb = mem_free / 1024.0 / 1024;
        float mem_used_gb = mem_total_gb - mem_free_gb;
        float mem_used_percent = (mem_used_gb / mem_total_gb) * 100.0;

        printf("Used Memory: %.2f%% (%.2f GB)\n\n", mem_used_percent, mem_used_gb);
        printf("Free Memory: %.2f GB (%.2f%%)\n", mem_free_gb, 100.0 - mem_used_percent);
        printf("Total Memory: %.2f GB\n", mem_total_gb);
    }

    //GPU INFORMATION
    printf("\n<--- GPU INFORMATION --->\n");
    FILE *fp2 = popen("lspci | grep -i 'vga\\|3d\\|2d'", "r");
    if (!fp2) {
        perror("Failed to detect GPU");
        return 0;
    }
    char line[256];
    int found_nvidia = 0, found_amd = 0, found_intel = 0;

    while(fgets(line, sizeof(line), fp2)) {
        if(strstr(line, "NVIDIA")) found_nvidia = 1;
        else if (strstr(line, "AMD") || strstr(line, "Radeon")) found_amd = 1;
        else if (strstr(line, "Intel")) found_intel = 1;
    }
    pclose(fp2);

    printf("GPU Usage: ");
    if (found_nvidia) {
        fp2 = popen("nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader", "r");
        if (fp2 && fgets(line, sizeof(line), fp2)) {
            printf("%s", line);
        }
        pclose(fp2);
    } else if (found_amd) {
        fp2 = popen("amdgpu_top --once | grep 'gpu' | head -n 1", "r");
        if (fp2 && fgets(line, sizeof(line), fp2)) {
            printf("%s", line);
        }
        pclose(fp2);
    } else if (found_intel) {
        fp2 = popen("intel_gpu_top -J -s 1000 | grep 'render busy'", "r");
        if (fp2 && fgets(line, sizeof(line), fp2)) {
            printf("%s", line);
        }
        pclose(fp2);
    } else {
        printf("No GPU Detected\n");
    }
    printf("\n");
    
    return 0;
}