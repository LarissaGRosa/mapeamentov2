  function getprofile(obj){
       obj1 = obj.value
       $.ajax({
                type:'POST',
                url:'get_professor',
                data:{

                    id : obj1,
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                    action: 'post'
                },
            success:function(json){
              $('#nome2').val(json.nome);
              $('#ensinomedio2').val(json.nome);
              $('#iniciomagis2').val(json.iniciomagis);
              document.getElementById('idprof').innerHTML = obj1;
               },
            error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
        });
        return obj1
    };

      function getprofile1(obj){
       obj1 = obj.value
       $.ajax({
                type:'POST',
                url:'get_professor1',
                data:{

                    id : obj1,
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                    action: 'post'
                },
            success:function(json){
              $('#nome2').val(json.nome);
              $('#ensinomedio2').val(json.nome);
              $('#iniciomagis2').val(json.iniciomagis);
              document.getElementById('idprof').innerHTML = obj1;
               },
            error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
        });
        return obj1
    };

    function getprofile_e(obj){
       obj1 = obj.value
       $.ajax({
                type:'POST',
                url:'getescola',
                data:{

                    id : obj1,
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                    action: 'post'
                },
            success:function(json){
              $('#nome3').val(json.nome);
              $('#dependencia3').val(json.dependencia);
              $('#municipio3').val(json.municipio);
              $('#regiao3').val(json.regiao);
              $("#uf3").val(json.uf);
              $("cod_municipio3").val(json.cod_municipio);
              document.getElementById('idesc').innerHTML = obj1;
               },
            error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
        });
        return obj1
    };
  function desativar(obj){
       obj1 = obj.value
       $.ajax({
                type:'POST',
                url:'desativarprofessor',
                data:{

                    id : obj1,
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                    action: 'post'
                },
            success:function(json){
              alert('Sucesso');
               },
            error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
        });
        return obj1
  };
  function desativar1(obj){
       obj1 = obj.value
       $.ajax({
                type:'POST',
                url:'desativarprofessor1',
                data:{

                    id : obj1,
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                    action: 'post'
                },
            success:function(json){
              alert('Sucesso');
               },
            error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
        });
        return obj1
  };

   function desativar_e(obj){
       obj1 = obj.value
       $.ajax({
                type:'POST',
                url:'desativarescola',
                data:{

                    id : obj1,
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                    action: 'post'
                },
            success:function(json){
              alert('Sucesso');
               },
            error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
        });
        return obj1
  };

  function desativar_pergunta(obj){
       obj1 = obj.value
       $.ajax({
                type:'POST',
                url:'desativarpergunta',
                data:{

                    id : obj1,
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                    action: 'post'
                },
            success:function(json){
              alert('Sucesso');
               },
            error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
        });
        return obj1
  };

  function desativar_postagem(obj){
       obj1 = obj.value
       $.ajax({
                type:'POST',
                url:'desativarpostagem',
                data:{

                    id : obj1,
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                    action: 'post'
                },
            success:function(json){
              alert('Sucesso');
               },
            error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
        });
        return obj1
  };










