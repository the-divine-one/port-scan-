import socket
import sys
import time

def resolve_target(target):
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print("[-] Hedef çözümlenemedi.")
        sys.exit(1)
#Kullanıcının verdiği domain ismini ipv4 adresine çevir
def get_service(port):
    try:
        return socket.getservbyport(port)
    except:
        return "bilinmiyor"
#port adreslerinin bilinen isimlerini verir ve eğer bilinen ismi bulamaz ise "bilinmiyo " diye döndürür


def scan_port(ip, port, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
#port adresini taramak için socketi belirliyoruz
    result = s.connect_ex((ip, port))
    s.close()
    if result == 0:
        return "açık"
    else:
        return "kapalı"
    #connect_ex ile portun açık olup olmadığını kontrol ediyoruz 


def scan(target, start_port, end_port, timeout=1):
    ip = resolve_target(target)
    #hedefi belirlediğimiz ip ve belirlediğimiz port aralığına göre tarar 

    print(f"\nTarget : {target} ({ip})")
    print(f"Ports  : {start_port}-{end_port}")
    print("Scan   : TCP Connect Scan")
    print("\nPORT     STATE   SERVICE")
    print("--------------------------------")
    #çok havalı duran bir açıklama tablosu sadece gösteriş amaçlı
    open_count = 0
    #belirlediğimiz başlangıç portunadan son porta kadar (son port dahil) tarama yapmak için if döngüsüne aldık 
    for port in range(start_port, end_port + 1):
        state = scan_port(ip, port, timeout)
        #portu tarar ve açık olup olmadığını söyler 
        if state == "open":
            service = get_service(port)
            print(f"{port:<8} {state:<7} {service}")
            open_count += 1
        #burda eğer açık ise bilgilerini ekrana veriyor 

    print("--------------------------------")
    print(f"Tarama tamamlandı, açık portlar : {open_count}\n")
    #ekrana bütün açık portları veriyor

if __name__ == "__main__":
    #eğer ilk denemenizde dümdüz çalıştırırsanız bu devreye giriyor
    banner()

    if len(sys.argv) != 4:
        print("Kullanım:")
        print("python scanner.py <hedef> <başlangıç_port> <bitiş_port>")
        print("Örnek:")
        print("python scanner.py 127.0.0.1 1 1024")
        sys.exit(1)
    #örnek kullanım anlamanız için 

    target = sys.argv[1]
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])

    start_time = time.time()
    scan(target, start_port, end_port)
    print(f"Elapsed time: {round(time.time() - start_time, 2)} seconds")
    #tarama zamanını ölçer (hocam neden eklediğimi sormayın)
#hocam hepsini tek tek anlatırım bence çok iyi bir kod olmuştur güveniyorum kendime 