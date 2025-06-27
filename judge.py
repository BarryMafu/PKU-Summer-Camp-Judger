import os
import subprocess
import psutil
import time
from enum import Enum
from dataclasses import dataclass

@dataclass
class Config:
    year: int = 2024
    problems: str = "A"

class Verdict(Enum):
    AC = "Accepted"
    WA = "Wrong Answer"
    CE = "Compile Err"
    TLE = "Time Lim Exc"
    MLE = "Memory Lim Exc"
    RE = "Runtime Error"

def compile_code(source_file, executable_file):
    try:
        result = subprocess.run(
            ["g++", source_file, "-o", executable_file, "-std=c++11"],
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        if result.returncode != 0:
            return (False, result.stderr)
        return (True, "Compilation successful")
    except Exception as e:
        return (False, str(e))

def run_code(executable_file, input_file, output_file, time_limit, memory_limit):
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            start_time = time.time()
            process = subprocess.Popen(
                [executable_file],
                stdin=infile,
                stdout=outfile,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            try:
                # 监控内存使用和超时
                peak_memory = 0
                ps_process = psutil.Process(process.pid)
                
                while process.poll() is None:
                    try:
                        # 检查是否超时
                        current_time = time.time()
                        elapsed_time = current_time - start_time
                        if elapsed_time > time_limit:
                            process.kill()
                            return (Verdict.TLE, f"TLE ({elapsed_time:.3f}s > {time_limit}s)", time_limit)
                        
                        # 检查内存使用
                        mem_info = ps_process.memory_info()
                        current_mem = mem_info.rss / (1024 * 1024)  # 转换为MB
                        peak_memory = max(peak_memory, current_mem)
                        
                        if peak_memory > memory_limit:
                            process.kill()
                            return (Verdict.MLE, f"MLE ({peak_memory:.2f}MB > {memory_limit}MB)", elapsed_time)
                            
                        time.sleep(0.01)  # 避免CPU占用过高
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        break
                
                # 等待进程结束（应该在超时或内存超限时已终止）
                process.wait(timeout=0)
                end_time = time.time()
                execution_time = end_time - start_time
                
                # 如果进程被杀死（超时或内存超限），已经返回结果
                # 这里处理正常结束的情况
                if process.returncode != 0:
                    return (Verdict.RE, f"RE (return code {process.returncode})", execution_time)
                
                return (Verdict.AC, "Correct!", execution_time)
            except subprocess.TimeoutExpired:
                # 这里处理wait(timeout=0)超时的情况，但理论上不应该发生
                process.kill()
                return (Verdict.TLE, "TLE (fallback)", time_limit)
    except MemoryError:
        return (Verdict.MLE, "MLE", 0)
    except Exception as e:
        return (Verdict.RE, f"RE: {str(e)}", 0)

def compare_outputs(user_output, expected_output):
    with open(user_output, 'r') as f1, open(expected_output, 'r') as f2:
        user_lines = [line.strip() for line in f1.readlines()]
        expected_lines = [line.strip() for line in f2.readlines()]
        
        if len(user_lines) != len(expected_lines):
            return False
        
        for u_line, e_line in zip(user_lines, expected_lines):
            if u_line != e_line:
                return False
        return True

def judge_single(year, problem, time_limit, memory_limit):
    source_file = f"Summer Camp {year}/Problem {problem}/solution.cpp"
    executable_file = f"Summer Camp {year}/Problem {problem}/solution.exe"
    user_output_file = f"Summer Camp {year}/Problem {problem}/output.txt"
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(source_file), exist_ok=True)
    
    compile_success, compile_message = compile_code(source_file, executable_file)
    if not compile_success:
        return {'verdict': Verdict.CE.value, 'message': compile_message}
    
    input_file = f"Summer Camp {year}/Problem {problem}/input.txt"
    expected_output_file = f"Summer Camp {year}/Problem {problem}/answer.txt"
    
    verdict, message, exec_time = run_code(
        executable_file, 
        input_file, 
        user_output_file,
        time_limit,
        memory_limit
    )
    
    if verdict == Verdict.AC:
        if compare_outputs(user_output_file, expected_output_file):
            return {'verdict': Verdict.AC.value, 'message': message, 'time': exec_time}
        else:
            return {'verdict': Verdict.WA.value, 'message': "WA"}
    else:
        return {'verdict': verdict.value, 'message': message}
    
def judge(year, problems):
    time_memory_limit_file = f"Summer Camp {year}/time_memory_limit.txt"
    if not os.path.exists(time_memory_limit_file):
        raise FileNotFoundError(f"Time and memory limit file not found for year {year}")
    time_memory_limit_dict = {}
    with open(time_memory_limit_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                problem_id, time_limit, memory_limit = parts
                time_memory_limit_dict[problem_id] = (int(time_limit), int(memory_limit))
            else:
                raise ValueError(f"Invalid format in time_memory_limit.txt: {line.strip()}")
            
    results = {}
    for problem in problems:
        if problem not in time_memory_limit_dict:
            raise ValueError(f"Problem {problem} not found in time_memory_limit.txt for year {year}")
        time_limit, memory_limit = time_memory_limit_dict[problem]
        results[problem] = judge_single(year, problem, time_limit, memory_limit)

    return results

def get_colorful_result(verdict):
    if verdict == Verdict.AC.value:
        return "\033[94m" + verdict + "\033[0m"  # 蓝色 - AC
    elif verdict == Verdict.CE.value:
        return "\033[32m" + verdict + "\033[0m"  # 深绿色 - CE
    else:
        return "\033[91m" + verdict + "\033[0m"  # 红色 - 其他错误类型

if __name__ == "__main__":
    config = Config()
    results = judge(config.year, config.problems)
    print(f"Judging results for Summer Camp {config.year}:")
    for problem, result in results.items():
        verdict = get_colorful_result(result['verdict'])
        time_info = f"{result.get('time', 0):.3f}s" if 'time' in result else "None"
        print(f"Problem {problem}: \t{verdict} \tTime: {time_info} \tMessage: {result.get('message', '')}")