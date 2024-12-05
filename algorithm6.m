function [bestchange, sku2] = algorithm6(A,B,C,sourcerack,targetrack,tabulist)
bestchange = 10000000;
list = find(C(:,sourcerack)==1).';
if sum(~ismember(list,tabulist)) == 0
    sku = list(randperm(length(list),1));
    change = algorithm4(A, B, C, sourcerack, targetrack, sku);
    if change < bestchange
        bestchange = change;
        sku2 = sku;
    end
else
    for sku = list
        if ~ismember(sku,tabulist)
            change = algorithm4(A, B, C, sourcerack, targetrack, sku);
            if change < bestchange
                bestchange = change;
                sku2 = sku;
            end
        end
    end
end