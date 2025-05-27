x = 5
y = 4.5
flag = true

function checar(z)
    if z > 10
        println("A soma é maior que 10")
    else
        println("A soma é menor ou igual a 10")
    end
end

for i in 1:10
    z = x + y + i / 2
    checar(z)
end

println("Resultado: ", z)