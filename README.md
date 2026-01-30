<a id="readme-top"></a>

<br />
<div align="center">
  <a href="https://github.com/nymaa999/car_market">
    <img src="images/logo.png" alt="Logo" width="100" height="100">
  </a>

  <h3 align="center">Car Market System</h3>

  <p align="center">
    Машины зар, үнэлгээний нэгдсэн систем
    <br />
    <a href="#api-documentation"><strong>API documentation »</strong></a>
    <br />
    <br />
    <a href="https://github.com/nymaa999/car_market">View Demo</a>
    &middot;
    <a href="https://github.com/nymaa999/car_market/issues">Report Bug</a>
  </p>
</div>

<details>
  <summary>Агуулга</summary>
  <ol>
    <li>
      <a href="#системийн-тухай">Системийн тухай</a>
      <ul>
        <li><a href="#ашигласан-технологиуд">Ашигласан технологиуд</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#суулгах">Суулгах</a></li>
      </ul>
    </li>
    <li>
        <a href="#deployment">Deployment</a>
        <ul>
            <li><a href="#орчин-бэлдэх">Орчин бэлдэх</a></li>
            <li><a href="#deploy">Deploy</a></li>
      </ul>
    </li>
    <li>
        <a href="#ашиглах">Ашиглах</a>
        <ul>
            <li><a href="#seller-борлуулагч">Seller (Борлуулагч)</a></li>
            <li><a href="#buyer-худалдан-авагч">Buyer (Худалдан авагч)</a></li>
            <li><a href="#admin-админ">Admin (Админ)</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## Системийн тухай

<div align="center">
  <img src="images/screenshot.png" alt="App Screenshot" width="80%" height="80%">
</div>

Энэхүү систем нь **машин худалдаа, үнэлгээний цогц платформ** бөгөөд Машин зарах сонирхолтой иргэд (Seller), машин хайж буй хэрэглэгчид (Buyer) болон системийн админуудад зориулагдсан.

**Үндсэн боломжууд:**
* **Seller:** Машины зар оруулах (зураг, үзүүлэлт), зарын төлөвийг хянах, профайл үүсгэх.
* **Buyer:** Машин хайх (шүүлтүүр ашиглан), дэлгэрэнгүй мэдээлэл харах, үнэлгээ (Review) бичих, дуртай зараа хадгалах.
* **Admin:** Шинэ заруудтай танилцаж баталгаажуулах (Workflow: Draft -> Pending -> Approved).

Системийг Frappe Desk UI дээр ашиглахаас гадна, гар утасны аппликейшн болон веб сайтад зориулсан бүрэн хэмжээний REST API-тай.

### Ашигласан технологиуд

* [![Frappe Framework](https://img.shields.io/badge/Frappe_Framework-000000?style=for-the-badge&logo=frappe&logoColor=white)](https://frappe.io/framework)
* ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
* ![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
* ![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)

## Getting Started

### Prerequisites

* [Frappe фреймворк суулгах](https://docs.frappe.io/framework/user/en/installation)
* Python 3.10+
* NodeJS 18+

### Суулгах

1.  **Bench эхлүүлэх**
    ```sh
    bench start
    ```
2.  **Github-аас апп татах**
    ```sh
    bench get-app [https://github.com/nymaa999/car_market.git](https://github.com/nymaa999/car_market.git)
    ```
3.  **Шинэ сайт үүсгэх (хэрэв үүсгээгүй бол)**
    ```sh
    bench new-site cars.local
    ```
4.  **Аппыг сайт руу суулгах**
    ```sh
    bench --site cars.local install-app car_market
    ```
5.  **Өгөгдлийн баазыг шилжүүлэх (Migrate)**
    ```sh
    bench --site cars.local migrate
    ```
6.  **Хөгжүүлэлтийн горимд ажиллуулах**
    ```sh
    bench start
    ```

## Deployment

### Орчин бэлдэх
Deploy хийхэд сервер дээр Docker суулгасан байх шаардлагатай.

1.  **Docker суулгах (Ubuntu)**
    ```sh
    sudo apt-get update
    sudo apt-get install ca-certificates curl gnupg
    # ... (Docker суулгах албан ёсны коммандууд) ...
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```

### Deploy
1.  **Docker Compose эхлүүлэх**
    ```sh
    docker compose up -d
    ```
2.  **Custom Image үүсгэх (Optional)**
    `apps.json` файл үүсгэж өөрийн repo-г зааж өгнө:
    ```json
    [
      {
        "url": "[https://github.com/nymaa999/car_market.git](https://github.com/nymaa999/car_market.git)",
        "branch": "main"
      }
    ]
    ```
3.  **Image Build хийх**
    ```sh
    export APPS_JSON_BASE64=$(base64 -w 0 apps.json)
    docker build \
      --build-arg=APPS_JSON_BASE64=$APPS_JSON_BASE64 \
      --tag=car-market-image .
    ```

## Ашиглах

### Seller (Борлуулагч)
Борлуулагч нь системд бүртгүүлж, өөрийн "Seller Profile"-ийг үүсгэсний дараа машин зарах эрхтэй болно.
1.  **Профайл үүсгэх:** `Seller Profile` хэсэгт өөрийн мэдээллийг оруулна.
2.  **Зар оруулах:** `Car Listing` > `Add Car Listing`.
    * Машины брэнд, загвар, он, үнэ, гүйлт зэргийг оруулна.
    * Зураг хавсаргана.
    * *Save* дарахад төлөв **Draft** байна.
3.  **Илгээх:** *Submit for Approval* товчийг дарснаар зар **Pending Review** төлөвт шилжиж Админ хянахыг хүлээнэ.

### Buyer (Худалдан авагч)
Худалдан авагч нь веб эсвэл мобайл апп ашиглан заруудтай танилцана.
* **Хайлт:** Үнэ, брэнд, он зэргээр шүүлтүүр хийх.
* **Review:** Зөвхөн баталгаажсан (Approved) заруудад үнэлгээ өгч, сэтгэгдэл бичих боломжтой.
* **Хадгалах:** Сонирхсон зараа "Saved Listings" рүү нэмэх.

### Admin (Админ)
Админ нь системийн үйл ажиллагааг хянана.
* **Зарыг батлах:** `Car Listing` жагсаалтаас "Pending Review" төлөвтэй заруудыг шалгаж **Approve** (Нийтэд харагдана) эсвэл **Reject** (Засах шаардлагатай) хийнэ.
* **Хэрэглэгчийн удирдлага:** Зүй бус сэтгэгдэл эсвэл хуурамч зарыг устгах.

## Contact
Хөгжүүлэгч: Nyamdorj
Email: dorjderemnymdorj81@gmail.com
Project Link: [https://github.com/nymaa999/car-market-backend.git](https://github.com/nymaa999/car-market-backend.git)

<p align="right">(<a href="#readme-top">back to top</a>)</p>