# AECPorto - CATS creating hours

Este script serve para registar Log activities, para doublecheck é reproduzido tudo o Fluxo existente no website. Os logs são realizados aleatoriamente no intervalo de tempo de **45** a **210** segundos, sendo que este valor poderá ser editado no codigo.

1. Adicionar ao browser uma extensão de gestão de cookies (exemplo CookieManager - Cookie Editor)
   
![Cookie Manager](https://github.com/JoseAbreu28/AECPorto/blob/efab98d873dcf8a80f46ffdb8eadb1cdb9dcc4d9/cookieManager.png)


2. Após login, abrir um Study Guide , obter a cookie **cats_wbt_session** assim como o **X-AUTH-TOKEN**

  ![Get Cookies](https://github.com/JoseAbreu28/AECPorto/blob/efab98d873dcf8a80f46ffdb8eadb1cdb9dcc4d9/2025-02-25_19-27.png)
  
5. Correr Script via PowerShell

   <code> python.exe .\aecporto_cats1.py</code>
   
