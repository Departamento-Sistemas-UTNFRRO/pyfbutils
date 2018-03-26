# -*- coding: utf-8 -*-

import urllib.request
import bs4
import pandas as pd
import os
import csv


def getHtml(url):
    req = urllib.request.Request(url)
    try:
        resp = urllib.request.urlopen(req)
    except Exception as ex:
        print("ERROR" + str(ex))
        return None
    else:
        html = resp.read()
        soup = bs4.BeautifulSoup(html, 'html.parser')
        return soup


def getHtml2(url):

    req = urllib.request.Request(url)
    try:
        resp = urllib.request.urlopen(req)
    except Exception as ex:
        print("ERROR" + str(ex))
        return None
    else:
        html = resp.read()
        return html


def getTituloFacebook(url):
    html = getHtml2(url)
    titulo = ""
    mencionesLista = []
    hashtagsLista = []

    if (html is not None):
        # El html de facebook viene en una etiqueta "code" comentada y se arma dinamico con Javascript
        # para poder interpretarlo, sacamos el comentario y lo pasamos normalmente al parseador
        # Por ejemplo:
        # <div class="hidden_elem"><code id="u_0_q"><!-- <div class="_5pcb _3z-f"> --></code>

        html = html.replace(b'<!--', b'')  # Apertura comentario
        html = html.replace(b'-->', b'')  # Cierre Comentario
        content = bs4.BeautifulSoup(html, 'lxml')
        # devuelve todos los titulos del los post del html, el que busco esta primero
        a = content.find_all('div', {'class': 'mbs _6m6 _2cnj _5s6c'})

        # Si la lista no esta vacia, tengo un titulo
        if a:
            titulo = a[0].getText()

        # Obtengo el bloque del html del post_message del post buscado
        post_message_html = content.find_all('div', {'class': '_5pbx userContent'})

        for tag in post_message_html:
            menciones = tag.find_all('a', {'class': 'profileLink'})
            for mencion in menciones:
                mencionesLista.append(mencion.getText())
            print(mencionesLista)
            hashtags = tag.find_all('span', {'class': '_58cm'})
            for hashtag in hashtags:
                hashtagsLista.append(hashtag.getText())

    # Devuelvo una tupla con los datos del post
    return (titulo, mencionesLista, hashtagsLista)


def loadCsvIntoDataSet(nombreArchivoEntrada):
    csv = pd.read_csv(nombreArchivoEntrada, header=0, sep=',', quotechar='\"', encoding="utf-8")
    return csv.values


def addColumnaTituloFacebook(nombreArchivoEntrada):
    posts = loadCsvIntoDataSet(nombreArchivoEntrada).tolist()

    for i in range(0, len(posts) - 1):
        try:
            # print(posts[i][2])
            url = posts[i][2]
            datosPost = getTituloFacebook(url)
            posts[i].append(datosPost[0])
            posts[i].append(datosPost[1])
            posts[i].append(datosPost[2])
        except Exception as ex:
            print(ex)
            columnas = len(posts[i]) + 1
            for j in range(columnas, 9):
                posts[i].append("Error exception")
    return posts


def saveInCsv(postsFinal, nombreArchivoSalida):
    columns = ['tipo_post', 'post_id', 'post_link', 'link', 'link_domain', 'titulo_facebook', 'menciones_facebook', 'hashtags_facebook']
    df = pd.DataFrame(data=postsFinal, columns=columns)
    df.to_csv(nombreArchivoSalida, index=False, columns=columns, sep=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)


# programaPrincipal
nombreArchivoEntrada = os.path.join(os.path.dirname(__file__), 'data', 'Todos_7_columnas.csv')
nombreArchivoSalida = os.path.join(os.path.dirname(__file__), 'data', 'Todos_7_columnas_salida.csv')
postsConTitulo = addColumnaTituloFacebook(nombreArchivoEntrada)
saveInCsv(postsConTitulo, nombreArchivoSalida)

# <div class="hidden_elem" id="toolbarContainer"></div>,
# <div class="hidden_elem"><code id="u_0_q"><!-- 
# <div class="_5pcb _3z-f"><div role="feed"><div class="_4-u2 mbm _4mrt _5jmm _5pat _5v3q _5uun _4-u8" data-ft="&#123;&quot;fbfeed_location&quot;:5&#125;" data-fte="1" data-ftr="1" data-testid="fbfeed_story" id="u_0_j"><div class="_3ccb" data-ft="&#123;&quot;tn&quot;:&quot;-R&quot;&#125;" data-gt="&#123;&quot;type&quot;:&quot;click2canvas&quot;,&quot;fbsource&quot;:703,&quot;ref&quot;:&quot;nf_generic&quot;&#125;" id="u_0_k"><div></div><div class="_5pcr userContentWrapper" data-ft="&#123;&quot;tn&quot;:&quot;-R&quot;&#125;"><div class="_1dwg _1w_m _q7o"><div class="_4r_y"><div></div></div><div><span class="_47we _42b7"></span><div class="_5x46"><div class="clearfix _5va3"><a class="_5pb8 _8o _8s lfloat _ohe" aria-hidden="true" tabindex="-1" target="" data-ft="&#123;&quot;tn&quot;:&quot;\\u003C&quot;&#125;" href="https://www.facebook.com/lanacion/?ref=nf&amp;hc_ref=ARR3gEOy_4Pcl6lmJj8jkE1fDmxYlO3AjHpteCKzc3Xn6oewoB6Z0BF9Pte-N1cH6rI"><div class="_38vo"><img class="_s0 _4ooo _5xib _5sq7 _44ma _rw img" src="https://scontent-eze1-1.xx.fbcdn.net/v/t1.0-1/p50x50/12009743_10153220885649220_4973571031869390011_n.png?oh=2c9c78850631cd3cf4ec1062e274a881&amp;oe=5AA2D1D2" alt="" aria-label="LA NACION" role="img" /></div></a><div class="clearfix _42ef"><div class="rfloat _ohf"></div><div class="_5va4"><div><div class="_6a _5u5j"><div class="_6a _6b" style="height:40px"></div><div class="_6a _5u5j _6b"><h5 class="_5pbw _5vra" data-ft="&#123;&quot;tn&quot;:&quot;C&quot;&#125;"><span class="fwn fcg"><span class="fwb fcg" data-ft="&#123;&quot;tn&quot;:&quot;k&quot;&#125;"><a href="https://www.facebook.com/lanacion/?hc_ref=ARRFktp0TpVHAVvI8Se2FzGMEkSH2wEm5iRRHShDXajRkk6nBQZsF8RKay4dxo5ic2Q&amp;fref=nf">LA NACION<a href="https://www.facebook.com/lanacion/?hc_ref=ARRFktp0TpVHAVvI8Se2FzGMEkSH2wEm5iRRHShDXajRkk6nBQZsF8RKay4dxo5ic2Q&amp;fref=nf"><span data-hover="tooltip" data-tooltip-position="right" class="_56_f _5dzy _5dz- _3twv" id="u_0_m"></span></a></a></span></span></h5><div class="_5pcp _5lel" id="feed_subtitle_71339054219;396647573684007;;9"><span class="_5paw _14zs" data-ft="&#123;&quot;tn&quot;:&quot;j&quot;&#125;"><a class="_3e_2 _14zr" href="#"></a></span><span role="presentation" aria-hidden="true"> · </span><span><span class="fsm fwn fcg"><a class="_5pcq" href="/lanacion/posts/396647573684007" target=""><abbr title="domingo, 19 de febrero de 2012 a las 8:08" data-utime="1329667734" data-shorten="1" class="_5ptz"><span class="timestampContent">19 de febrero de 2012</span></abbr></a></span></span><span role="presentation" aria-hidden="true"> · </span><a data-hover="tooltip" data-tooltip-content="P&#xfa;blico" class="uiStreamPrivacy inlineBlock fbStreamPrivacy fbPrivacyAudienceIndicator _5pcq" aria-label="P&#xfa;blico" href="#" role="button"><i class="lock img sp_BFOmfqqJB5L sx_a75914"></i></a></div></div></div></div></div></div></div></div><div class="_5pbx userContent" data-ft="&#123;&quot;tn&quot;:&quot;K&quot;&#125;"><p>¿Qué pensás de la medidda? Enterate porque lo hizo ingresando a la nota</p></div><div class="_3x-2"><div data-ft="&#123;&quot;tn&quot;:&quot;H&quot;&#125;"><div class="mtm"><div id="u_0_l" class="_6m2 _1zpr clearfix _dcs _4_w4 _5cwb _5qqr" 
# data-ft="&#123;&quot;tn&quot;:&quot;H&quot;&#125;">
# <div class="clearfix _2r3x"><div class="lfloat _ohe">
# <span class="_3m6-"><div class="_6ks"><a href="https://l.facebook.com/l.php?u=http%3A%2F%2Fwww.lanacion.com.ar%2F1450049-purga-en-gendarmeria-garre-paso-a-retiro-a-19-comandantes&amp;h=ATNnXrckg8L0t0lalGO-tLbXtKARcFIvIz6DeV_IW6tOzyoDPzm6hAdfMLkC3StWZgVQ3qgkRynCkHU7R6SkvKNhgRyl5NjbdbMuwyszE_zND4XAGFyuA-M4GHhAHiCd14KK_ZpXV0UBe9PtdY9onic9HhsNOgy2acy_yPaJ4j8nlpDSW_W4a8qFM_5BVuv9Q0CxfyrZDEqjdJ7JQfeldhAhYH3LZLL3-KUXZHsEE9w5gAK0Is7HDYMZ9hgPHOPRkx4_x4o1D-f-" tabindex="-1" target="_blank" data-lynx-mode="hover" rel="nofollow"><div class="_6l- __c_"><div class="uiScaledImageContainer _6m5 fbStoryAttachmentImage" style="width:158px;height:158px;"><img class="scaledImageFitWidth img" src="https://external-eze1-1.xx.fbcdn.net/safe_image.php?d=AQAq5kStMs9BLmqO&amp;w=160&amp;h=160&amp;url=http%3A%2F%2Fbucket.clanacion.com.ar%2Fanexos%2Ffotos%2F50%2F1498250.jpg&amp;cfs=1&amp;upscale=1&amp;fallback=news_d_placeholder_publisher&amp;_nc_hash=AQA3FtEddNQUE5I0" alt="" width="158" height="158" /></div></div></a></div></span></div><div class="_42ef"><span class="_3c21"><div class="_3ekx _29_4"><div class="_6m3 _-\-\6"><div class="mbs _6m6 _2cnj _5s6c"><a href="https://l.facebook.com/l.php?u=http%3A%2F%2Fwww.lanacion.com.ar%2F1450049-purga-en-gendarmeria-garre-paso-a-retiro-a-19-comandantes&amp;h=ATN714kM6spBNeAZxGcZl5K_pGik5hEaMJAhuwcZU8PxTWKs-rIsqonct1rwjGDlh6Bid9_pK1a2f6KLqWUui4qHfk0IzE-P2eXa7_CUbFfJphz3Mh0IZbltvw-DFVVQMi5ADt9uin5nabOIJgDR6oIBquPAQD_SY0NlhpHKcfE4rc250r3uI2VChg03T2SD9G30LPuTb_MXSVYfOkm9c3yC8A0WtcdSZJW6tZmqR9BTwJDdkqfhZwLohxgLIxjDlbdtXrbgzBN3" rel="nofollow" target="_blank" data-lynx-mode="hover">Purga en Gendarmería: Garré pasó a retiro a 19 comandantes</a></div><div class="_6m7 _3bt9"></div><div class="_59tj _2iau"><div><div class="_6lz _6mb ellipsis">lanacion.com.ar</div><div class=""></div></div></div></div><a class="_52c6" href="https://l.facebook.com/l.php?u=http%3A%2F%2Fwww.lanacion.com.ar%2F1450049-purga-en-gendarmeria-garre-paso-a-retiro-a-19-comandantes&amp;h=ATO_3XUA68AXWWd76Vnsh4LrG9iGIUj5LoQ8C7eCxLrBJRQNHAv9rAXooii7dbFNcqFuOCW7HDDZotVdB1Ysbw4aC7fgjY8Koue6yB8CfYQqLCzqKp_erweG7-yDPBHrstkJzcuV083ug6zGLp1aMwdCgUM-eMmip6_-YynBzhhFl11-Ku-5qJAVdkOZ9ZjwOXWCRXjGZpp3zCszxsKVdbVLlbuPK8A-eMeEFBIkE0ShEPnL1-4gMoOPzLPrtmcBo_SSZg094exD" tabindex="-1" target="_blank" data-lynx-mode="hover" rel="nofollow"></a></div></span></div></div></div></div></div></div><div></div></div></div><div><form rel="async" class="commentable_item collapsed_comments" method="post" data-ft="&#123;&quot;tn&quot;:&quot;]&quot;&#125;" action="/ajax/ufi/modify.php" onsubmit="return window.Event &amp;&amp; Event.__inlineSubmit &amp;&amp; Event.__inlineSubmit(this,event)" id="u_0_o"><input type="hidden" name="lsd" value="AVrRnz6S" autocomplete="off" /><input type="hidden" autocomplete="off" name="ft_ent_identifier" value="396647573684007" /><input type="hidden" autocomplete="off" name="data_only_response" value="1" /><div class="_sa_ _gsd _5vsi _192z"><div class="_37uu"></div></div><div class="uiUfi UFIContainer _5pc9 _5vsj _5v9k" id="u_0_p"></div></form></div></div></div></div></div></div> --></code></div>, <div class="hidden_elem"><code id="u_0_u"><!-- <div class="_45mq"><div class="uiContextualLayerParent"><div class="_4-u2 _19ah _2ph_ _4-u8"><div class="_5aj7"><div class="_4bl9"><div class="fsm fwn fcg"><span lang="es_LA">Español</span><span role="presentation" aria-hidden="true"> · </span><a class="_5f4c" dir="ltr" href="#" lang="en_US" onclick="require(&quot;IntlUtils&quot;).setCookieLocale(&quot;en_US&quot;, &quot;es_LA&quot;, &quot;https:\\/\\/www.facebook.com\\/71339054219\\/posts\\/396647573684007&quot;, &quot;www_card_selector&quot;, 0); return false;" title="English (US)" role="button">English (US)</a><span role="presentation" aria-hidden="true"> · </span><a class="_5f4c" dir="ltr" href="#" lang="pt_BR" onclick="require(&quot;IntlUtils&quot;).setCookieLocale(&quot;pt_BR&quot;, &quot;es_LA&quot;, &quot;https:\\/\\/pt-br.facebook.com\\/71339054219\\/posts\\/396647573684007&quot;, &quot;www_card_selector&quot;, 1); return false;" title="Portuguese (Brazil)" role="button">Português (Brasil)</a><span role="presentation" aria-hidden="true"> · </span><a class="_5f4c" dir="ltr" href="#" lang="fr_FR" onclick="require(&quot;IntlUtils&quot;).setCookieLocale(&quot;fr_FR&quot;, &quot;es_LA&quot;, &quot;https:\\/\\/fr-fr.facebook.com\\/71339054219\\/posts\\/396647573684007&quot;, &quot;www_card_selector&quot;, 2); return false;" title="French (France)" role="button">Français (France)</a><span role="presentation" aria-hidden="true"> · </span><a class="_5f4c" dir="ltr" href="#" lang="de_DE" onclick="require(&quot;IntlUtils&quot;).setCookieLocale(&quot;de_DE&quot;, &quot;es_LA&quot;, &quot;https:\\/\\/de-de.facebook.com\\/71339054219\\/posts\\/396647573684007&quot;, &quot;www_card_selector&quot;, 3); return false;" title="German" role="button">Deutsch</a></div></div><div class="_4bl7 _2pit"><a class="_42ft _4jy0 _4jy4 _517h _51sy" role="button" ajaxify="/settings/language/language/?uri=https%3A%2F%2Fwww.facebook.com%2F71339054219%2Fposts%2F396647573684007&amp;source=www_card_selector_more" rel="dialog" href="#" aria-label="Usa Facebook en otro idioma."><i class="img sp_lbWj69LqQFT sx_21ec69"></i></a></div></div></div></div><div aria-label="Facebook" class="_26z1" role="contentinfo"><div class="fsm fwn fcg"><a href="https://www.facebook.com/privacy/explanation" title="Inf&#xf3;rmate acerca de tu privacidad y Facebook.">Privacidad</a><span role="presentation" aria-hidden="true"> · </span><a accesskey="9" href="https://www.facebook.com/policies?ref=pf" title="Consulta nuestras pol&#xed;ticas y condiciones.">Condiciones</a><span role="presentation" aria-hidden="true"> · </span><a href="https://www.facebook.com/campaign/landing.php?placement=pf_rhc&amp;campaign_id=242449722530626&amp;extra_1=auto" title="An&#xfa;nciate en Facebook.">Publicidad</a><span role="presentation" aria-hidden="true"> · </span><a class="_41uf" href="https://www.facebook.com/help/568137493302217" title="Conoce las opciones de anuncios.">Opciones de anuncios<i class="img sp_lbWj69LqQFT sx_f0fbad"></i></a><span role="presentation" aria-hidden="true"> · </span><a href="https://www.facebook.com/help/cookies?ref_type=sitefooter" title="Cookies">Cookies</a><span role="presentation" aria-hidden="true"> · </span><div class="_6a uiPopover" id="u_0_s"><a class="_45mr _p" aria-haspopup="true" aria-expanded="false" rel="toggle" href="#" role="button" id="u_0_t">Más<i class="img sp_lbWj69LqQFT sx_2e0acf"></i></a></div></div><div><span> Facebook © 2017</span></div></div></div> --></code></div>]
# <div class="hidden_elem" id="toolbarContainer"></div>
# <div class="hidden_elem"><code id="u_0_q"><!-- <div class="_5pcb _3z-f">
# <div role="feed"><div class="_4-u2 mbm _4mrt _5jmm _5pat _5v3q _5uun _4-u8" data-ft="&#123;&quot;fbfeed_location&quot;:5&#125;" data-fte="1" data-ftr="1" data-testid="fbfeed_story" id="u_0_j">
# <div class="_3ccb" data-ft="&#123;&quot;tn&quot;:&quot;-R&quot;&#125;" data-gt="&#123;&quot;type&quot;:&quot;click2canvas&quot;,&quot;fbsource&quot;:703,&quot;ref&quot;:&quot;nf_generic&quot;&#125;" id="u_0_k">
# <div></div><div class="_5pcr userContentWrapper" data-ft="&#123;&quot;tn&quot;:&quot;-R&quot;&#125;"><div class="_1dwg _1w_m _q7o"><div class="_4r_y"><div></div></div><div><span class="_47we _42b7"></span><div class="_5x46"><div class="clearfix _5va3"><a class="_5pb8 _8o _8s lfloat _ohe" aria-hidden="true" tabindex="-1" target="" data-ft="&#123;&quot;tn&quot;:&quot;\\u003C&quot;&#125;" href="https://www.facebook.com/lanacion/?ref=nf&amp;hc_ref=ARR3gEOy_4Pcl6lmJj8jkE1fDmxYlO3AjHpteCKzc3Xn6oewoB6Z0BF9Pte-N1cH6rI"><div class="_38vo"><img class="_s0 _4ooo _5xib _5sq7 _44ma _rw img" src="https://scontent-eze1-1.xx.fbcdn.net/v/t1.0-1/p50x50/12009743_10153220885649220_4973571031869390011_n.png?oh=2c9c78850631cd3cf4ec1062e274a881&amp;oe=5AA2D1D2" alt="" aria-label="LA NACION" role="img" /></div></a><div class="clearfix _42ef"><div class="rfloat _ohf"></div><div class="_5va4"><div><div class="_6a _5u5j"><div class="_6a _6b" style="height:40px"></div><div class="_6a _5u5j _6b"><h5 class="_5pbw _5vra" data-ft="&#123;&quot;tn&quot;:&quot;C&quot;&#125;"><span class="fwn fcg"><span class="fwb fcg" data-ft="&#123;&quot;tn&quot;:&quot;k&quot;&#125;"><a href="https://www.facebook.com/lanacion/?hc_ref=ARRFktp0TpVHAVvI8Se2FzGMEkSH2wEm5iRRHShDXajRkk6nBQZsF8RKay4dxo5ic2Q&amp;fref=nf">LA NACION<a href="https://www.facebook.com/lanacion/?hc_ref=ARRFktp0TpVHAVvI8Se2FzGMEkSH2wEm5iRRHShDXajRkk6nBQZsF8RKay4dxo5ic2Q&amp;fref=nf"><span data-hover="tooltip" data-tooltip-position="right" class="_56_f _5dzy _5dz- _3twv" id="u_0_m"></span></a></a></span></span></h5><div class="_5pcp _5lel" id="feed_subtitle_71339054219;396647573684007;;9"><span class="_5paw _14zs" data-ft="&#123;&quot;tn&quot;:&quot;j&quot;&#125;"><a class="_3e_2 _14zr" href="#"></a></span><span role="presentation" aria-hidden="true"> · </span><span><span class="fsm fwn fcg"><a class="_5pcq" href="/lanacion/posts/396647573684007" target=""><abbr title="domingo, 19 de febrero de 2012 a las 8:08" data-utime="1329667734" data-shorten="1" class="_5ptz"><span class="timestampContent">19 de febrero de 2012</span></abbr></a></span></span><span role="presentation" aria-hidden="true"> · </span><a data-hover="tooltip" data-tooltip-content="P&#xfa;blico" class="uiStreamPrivacy inlineBlock fbStreamPrivacy fbPrivacyAudienceIndicator _5pcq" aria-label="P&#xfa;blico" href="#" role="button"><i class="lock img sp_BFOmfqqJB5L sx_a75914"></i></a></div></div></div></div></div></div></div></div><div class="_5pbx userContent" data-ft="&#123;&quot;tn&quot;:&quot;K&quot;&#125;"><p>¿Qué pensás de la medidda? Enterate porque lo hizo ingresando a la nota</p></div><div class="_3x-2"><div data-ft="&#123;&quot;tn&quot;:&quot;H&quot;&#125;"><div class="mtm"><div id="u_0_l" class="_6m2 _1zpr clearfix _dcs _4_w4 _5cwb _5qqr" data-ft="&#123;&quot;tn&quot;:&quot;H&quot;&#125;"><div class="clearfix _2r3x"><div class="lfloat _ohe"><span class="_3m6-"><div class="_6ks"><a href="https://l.facebook.com/l.php?u=http%3A%2F%2Fwww.lanacion.com.ar%2F1450049-purga-en-gendarmeria-garre-paso-a-retiro-a-19-comandantes&amp;h=ATNnXrckg8L0t0lalGO-tLbXtKARcFIvIz6DeV_IW6tOzyoDPzm6hAdfMLkC3StWZgVQ3qgkRynCkHU7R6SkvKNhgRyl5NjbdbMuwyszE_zND4XAGFyuA-M4GHhAHiCd14KK_ZpXV0UBe9PtdY9onic9HhsNOgy2acy_yPaJ4j8nlpDSW_W4a8qFM_5BVuv9Q0CxfyrZDEqjdJ7JQfeldhAhYH3LZLL3-KUXZHsEE9w5gAK0Is7HDYMZ9hgPHOPRkx4_x4o1D-f-" tabindex="-1" target="_blank" data-lynx-mode="hover" rel="nofollow"><div class="_6l- __c_"><div class="uiScaledImageContainer _6m5 fbStoryAttachmentImage" style="width:158px;height:158px;"><img class="scaledImageFitWidth img" src="https://external-eze1-1.xx.fbcdn.net/safe_image.php?d=AQAq5kStMs9BLmqO&amp;w=160&amp;h=160&amp;url=http%3A%2F%2Fbucket.clanacion.com.ar%2Fanexos%2Ffotos%2F50%2F1498250.jpg&amp;cfs=1&amp;upscale=1&amp;fallback=news_d_placeholder_publisher&amp;_nc_hash=AQA3FtEddNQUE5I0" alt="" width="158" height="158" /></div></div></a></div></span></div><div class="_42ef"><span class="_3c21"><div class="_3ekx _29_4"><div class="_6m3 _-\-\6"><div class="mbs _6m6 _2cnj _5s6c"><a href="https://l.facebook.com/l.php?u=http%3A%2F%2Fwww.lanacion.com.ar%2F1450049-purga-en-gendarmeria-garre-paso-a-retiro-a-19-comandantes&amp;h=ATN714kM6spBNeAZxGcZl5K_pGik5hEaMJAhuwcZU8PxTWKs-rIsqonct1rwjGDlh6Bid9_pK1a2f6KLqWUui4qHfk0IzE-P2eXa7_CUbFfJphz3Mh0IZbltvw-DFVVQMi5ADt9uin5nabOIJgDR6oIBquPAQD_SY0NlhpHKcfE4rc250r3uI2VChg03T2SD9G30LPuTb_MXSVYfOkm9c3yC8A0WtcdSZJW6tZmqR9BTwJDdkqfhZwLohxgLIxjDlbdtXrbgzBN3" 
# rel="nofollow" target="_blank" data-lynx-mode="hover">Purga en Gendarmería: Garré pasó a retiro a 19 comandantes</a></div><div class="_6m7 _3bt9"></div><div class="_59tj _2iau"><div><div class="_6lz _6mb ellipsis">lanacion.com.ar</div><div class=""></div></div></div></div><a class="_52c6" href="https://l.facebook.com/l.php?u=http%3A%2F%2Fwww.lanacion.com.ar%2F1450049-purga-en-gendarmeria-garre-paso-a-retiro-a-19-comandantes&amp;h=ATO_3XUA68AXWWd76Vnsh4LrG9iGIUj5LoQ8C7eCxLrBJRQNHAv9rAXooii7dbFNcqFuOCW7HDDZotVdB1Ysbw4aC7fgjY8Koue6yB8CfYQqLCzqKp_erweG7-yDPBHrstkJzcuV083ug6zGLp1aMwdCgUM-eMmip6_-YynBzhhFl11-Ku-5qJAVdkOZ9ZjwOXWCRXjGZpp3zCszxsKVdbVLlbuPK8A-eMeEFBIkE0ShEPnL1-4gMoOPzLPrtmcBo_SSZg094exD" tabindex="-1" target="_blank" data-lynx-mode="hover" rel="nofollow"></a></div></span></div></div></div></div></div></div><div></div></div></div><div><form rel="async" class="commentable_item collapsed_comments" method="post" data-ft="&#123;&quot;tn&quot;:&quot;]&quot;&#125;" action="/ajax/ufi/modify.php" onsubmit="return window.Event &amp;&amp; Event.__inlineSubmit &amp;&amp; Event.__inlineSubmit(this,event)" id="u_0_o"><input type="hidden" name="lsd" value="AVrRnz6S" autocomplete="off" /><input type="hidden" autocomplete="off" name="ft_ent_identifier" value="396647573684007" /><input type="hidden" autocomplete="off" name="data_only_response" value="1" /><div class="_sa_ _gsd _5vsi _192z"><div class="_37uu"></div></div><div class="uiUfi UFIContainer _5pc9 _5vsj _5v9k" id="u_0_p"></div></form></div></div></div></div></div></div> --></code></div>
# <div class="hidden_elem"><code id="u_0_u"><!-- <div class="_45mq"><div class="uiContextualLayerParent"><div class="_4-u2 _19ah _2ph_ _4-u8"><div class="_5aj7"><div class="_4bl9"><div class="fsm fwn fcg"><span lang="es_LA">Español</span><span role="presentation" aria-hidden="true"> · </span><a class="_5f4c" dir="ltr" href="#" lang="en_US" onclick="require(&quot;IntlUtils&quot;).setCookieLocale(&quot;en_US&quot;, &quot;es_LA&quot;, &quot;https:\\/\\/www.facebook.com\\/71339054219\\/posts\\/396647573684007&quot;, &quot;www_card_selector&quot;, 0); return false;" title="English (US)" role="button">English (US)</a><span role="presentation" aria-hidden="true"> · </span><a class="_5f4c" dir="ltr" href="#" lang="pt_BR" onclick="require(&quot;IntlUtils&quot;).setCookieLocale(&quot;pt_BR&quot;, &quot;es_LA&quot;, &quot;https:\\/\\/pt-br.facebook.com\\/71339054219\\/posts\\/396647573684007&quot;, &quot;www_card_selector&quot;, 1); return false;" title="Portuguese (Brazil)" role="button">Português (Brasil)</a><span role="presentation" aria-hidden="true"> · </span><a class="_5f4c" dir="ltr" href="#" lang="fr_FR" onclick="require(&quot;IntlUtils&quot;).setCookieLocale(&quot;fr_FR&quot;, &quot;es_LA&quot;, &quot;https:\\/\\/fr-fr.facebook.com\\/71339054219\\/posts\\/396647573684007&quot;, &quot;www_card_selector&quot;, 2); return false;" title="French (France)" role="button">Français (France)</a><span role="presentation" aria-hidden="true"> · </span><a class="_5f4c" dir="ltr" href="#" lang="de_DE" onclick="require(&quot;IntlUtils&quot;).setCookieLocale(&quot;de_DE&quot;, &quot;es_LA&quot;, &quot;https:\\/\\/de-de.facebook.com\\/71339054219\\/posts\\/396647573684007&quot;, &quot;www_card_selector&quot;, 3); return false;" title="German" role="button">Deutsch</a></div></div><div class="_4bl7 _2pit"><a class="_42ft _4jy0 _4jy4 _517h _51sy" role="button" ajaxify="/settings/language/language/?uri=https%3A%2F%2Fwww.facebook.com%2F71339054219%2Fposts%2F396647573684007&amp;source=www_card_selector_more" rel="dialog" href="#" aria-label="Usa Facebook en otro idioma."><i class="img sp_lbWj69LqQFT sx_21ec69"></i></a></div></div></div></div><div aria-label="Facebook" class="_26z1" role="contentinfo"><div class="fsm fwn fcg"><a href="https://www.facebook.com/privacy/explanation" title="Inf&#xf3;rmate acerca de tu privacidad y Facebook.">Privacidad</a><span role="presentation" aria-hidden="true"> · </span><a accesskey="9" href="https://www.facebook.com/policies?ref=pf" title="Consulta nuestras pol&#xed;ticas y condiciones.">Condiciones</a><span role="presentation" aria-hidden="true"> · </span><a href="https://www.facebook.com/campaign/landing.php?placement=pf_rhc&amp;campaign_id=242449722530626&amp;extra_1=auto" title="An&#xfa;nciate en Facebook.">Publicidad</a><span role="presentation" aria-hidden="true"> · </span><a class="_41uf" href="https://www.facebook.com/help/568137493302217" title="Conoce las opciones de anuncios.">Opciones de anuncios<i class="img sp_lbWj69LqQFT sx_f0fbad"></i></a><span role="presentation" aria-hidden="true"> · </span><a href="https://www.facebook.com/help/cookies?ref_type=sitefooter" title="Cookies">Cookies</a><span role="presentation" aria-hidden="true"> · </span><div class="_6a uiPopover" id="u_0_s"><a class="_45mr _p" aria-haspopup="true" aria-expanded="false" rel="toggle" href="#" role="button" id="u_0_t">Más<i class="img sp_lbWj69LqQFT sx_2e0acf"></i></a></div></div><div><span> Facebook © 2017</span></div></div></div> --></code></div>
